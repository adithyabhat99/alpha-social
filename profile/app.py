from flask import Flask, request, jsonify, make_response
from flaskext.mysql import MySQL
import uuid
import datetime
import jwt
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'adi123secret'
UPLOAD_FOLDER = '/mnt/Users'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL Configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 52000
mysql.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message": "error:token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithm='SHA256')
        except:
            return jsonify({"message": "error:token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename):
    return filename.rsplit('.', 1)[1]


@app.route('/')
def hi():
    return jsonify({"mesage": "hi! welcome to profile server"}), 200


@app.route('/api/v1.0/update/profilepic', methods=['GET', 'POST'])
@token_required
def update(userid):
    if 'file' not in request.files:
        return jsonify({"message": "error:file required"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "error:file required"}), 401
    if file and allowed_file(file.filename):
        if file_extension(file.filename) == "png":
            im = Image.open(request.files['file'].stream)
            rgb_im = im.convert('RGB')
            filename = str(userid)+'.jpg'
            rgb_im.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), "JPEG")
            return jsonify({"message": "success!"}), 200
        filename = str(userid)+'.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "success!"}), 200
    return jsonify({"message": "error:unsuccessfull"}), 401


@app.route('/api/v1.0/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify 0', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    query = "select count(*) from users.user where username='{0}'".format(
        auth.username)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if result[0][0] != 1:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    query = "select userid,password from users.user where username='{0}'".format(
        auth.username)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    password = result[0][1]
    if check_password_hash(password, auth.password):
        token = jwt.encode({"userid": result[0][0], "username": auth.username, "exp": datetime.datetime.now(
        )+datetime.timedelta(days=7)}, app.secret_key, algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/api/v1.0/createuser', methods=['GET', 'POST'])
def create_user():
    data = request.get_json(force=True)
    print(data)
    if data is None:
        return jsonify({"message": "error:data required"}), 401
    if 'username' in data:
        username = data['username']
        query = "select count(*) from users.user where username='{0}'".format(
            username)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if result[0][0] != 0:
            return jsonify({"message": "error:username already exists"}), 401
    else:
        return jsonify({"mesage": "error:username is must"}), 401
    userid = uuid.uuid4()
    if 'password' in data:
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
    else:
        return jsonify({"mesage": "error:password is must"}), 401
    if 'firstname' in data:
        firstname = data['firstname']
    else:
        return jsonify({"mesage": "error:firstname is must"}), 401
    if 'lastname' in data:
        lastname = data['lastname']
    else:
        return jsonify({"mesage": "error:lastname is must"}), 401
    if 'bio' in data:
        bio = data['bio']
    else:
        bio = 'null'
    if 'phoneno' not in data and 'email' not in data:
        return jsonify({"message": "error:email or phoneno is must"}), 401
    if 'phoneno' in data:
        phoneno = data['phoneno']
    else:
        phoneno = '-'+str(userid)[0:10]
    if 'email' in data:
        email = data['email']
    else:
        email = '-'+str(userid)[0:10]
    if 'public' in data:
        public = data['public']
    else:
        public = '0'
    token = uuid.uuid4()
    phonetoken = uuid.uuid4()
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,bio) \
          values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}');".format(userid, username, firstname, lastname, hashed_password, email, phoneno,
                                                                                                            token, phonetoken, public, time, time, bio)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    filename = str(userid)+"jpg"

    return jsonify({"message": "success!"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7700)
