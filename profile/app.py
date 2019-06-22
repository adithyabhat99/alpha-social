from flask import Flask, request, jsonify, make_response, send_file
from flaskext.mysql import MySQL
import uuid
import datetime
import jwt
import os
import shutil
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image

app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'adi123secret'
USERS_FOLDER = '/mnt/Users'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])
app.config['USERS_FOLDER'] = USERS_FOLDER
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

def get_follow_count(userid):
    query="select count(*) from users.follow where followed='{0}'".format(userid)
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        return result[0][0]
    except:
        return 0


def get_following_count(userid):
    query="select count(*) from users.follow where follower='{0}'".format(userid)
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        return result[0][0]
    except:
        return 0

@app.route('/')
def hi():
    return jsonify({"mesage": "hi! welcome to profile server"}), 200


@app.route('/api/v1.0/update/bio', methods=['GET', 'POST'])
@token_required
def update_bio(userid):
    data = request.get_json(force=True)
    if not data or "new_bio" not in data:
        return jsonify({"message": "error:data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set bio='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_bio'], time, userid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/update/name', methods=['GET', 'POST'])
@token_required
def update_name(userid):
    data = request.get_json(force=True)
    if not data or "new_firstname" not in data or "new_lastname" not in data:
        return jsonify({"message": "error:data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set firstname='{0}',lastname='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_firstname'], data['new_lastname'], time, userid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/update/phoneno', methods=['GET', 'POST'])
@token_required
def update_phone(userid):
    data = request.get_json(force=True)
    if not data or "new_phoneno" not in data:
        return jsonify({"message": "error:data required"}), 401
    query = "select count(*) from users.user where phoneno='{0}'".format(
        data['new_phoneno'])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    if result[0][0] != 0:
        return jsonify({"message": "error:phoneno already exists"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set phoneno='{0}',verified='0',phonetoken='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_phoneno'], uuid.uuid4(), time, userid)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/update/email', methods=['GET', 'POST'])
@token_required
def update_email(userid):
    data = request.get_json(force=True)
    if not data or "new_email" not in data:
        return jsonify({"message": "error:data required"}), 401
    query = "select count(*) from users.user where email='{0}'".format(
        data['new_email'])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    if result[0][0] != 0:
        return jsonify({"message": "error:email already exists"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set email='{0}',verified='0',token='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_email'], uuid.uuid4(), time, userid)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/update/username', methods=['GET', 'POST'])
@token_required
def updatedetails(userid):
    data = request.get_json(force=True)
    if not data or "new_username" not in data:
        return jsonify({"message": "error:data required"}), 401
    query = "select count(*) from users.user where username='{0}'".format(
        data['new_username'])
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    if result[0][0] != 0:
        return jsonify({"message": "error:username already exists"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set username='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_username'], time, userid)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/update/profilepic', methods=['GET', 'POST'])
@token_required
def update(userid):
    if 'file' not in request.files:
        return jsonify({"message": "error:file required"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "error:file required"}), 401
    if file and allowed_file(file.filename):
        os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
        if file_extension(file.filename) == "png":
            im = Image.open(request.files['file'].stream)
            rgb_im = im.convert('RGB')
            filename = str(userid)+'.jpg'
            rgb_im.save(os.path.join(
                app.config['USERS_FOLDER'], filename), "JPEG")
        else:
            filename = str(userid)+'.jpg'
            file.save(os.path.join(app.config['USERS_FOLDER'], filename))
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "success!"}), 200
    else:
        return jsonify({"message": "error:unsuccessfull"}), 401


@app.route('/api/v1.0/update/deleteprofilepic', methods=['GET', 'POST'])
@token_required
def delpic(userid):
    os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
    filename = userid+".jpg"
    defaultfile = 'defualt.jpg'
    shutil.copy(os.path.join(app.config['USERS_FOLDER'], defaultfile), os.path.join(
        app.config['USERS_FOLDER'], filename))
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
        time, userid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "success!"}), 200


@app.route('/api/v1.0/getmyprofilepic', methods=['GET', 'POST'])
@token_required
def getmyprofilepic(userid):
    filename = os.path.join(app.config['USERS_FOLDER'], userid+".jpg")
    return send_file(filename, mimetype='image/gif')


@app.route('/api/v1.0/getmydetails', methods=['GET', 'POST'])
@token_required
def getmydetails(userid):
    query = "select * from users.user where userid='{0}'".format(userid)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    username = result[0][1]
    firstname = result[0][2]
    lastname = result[0][3]
    if result[0][7] == 1:
        email = result[0][5]
    else:
        email = None
    if result[0][10] == 1:
        phoneno = result[0][8]
    else:
        phoneno = None
    public = result[0][11]
    datecreated = result[0][12]
    dateupdated = result[0][13]
    if result[0][14] == 'null':
        bio = None
    else:
        bio = result[0][14]
    followerscount=get_follow_count(userid)
    followingcount=get_following_count(userid)
    details = {
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phoneno": phoneno,
        "public": public,
        "datecreated": datecreated,
        "dateupdated": dateupdated,
        "bio": bio,
        "followerscount":followerscount,
        "followingcount":followingcount
    }
    return jsonify(details), 200


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
        return jsonify({'token': token.decode('UTF-8')}), 200
    return make_response('Could not verify 2', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/api/v1.0/creataccount', methods=['GET', 'POST'])
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
    filename = str(userid)+".jpg"
    defaultfile = 'defualt.jpg'
    shutil.copy(os.path.join(app.config['USERS_FOLDER'], defaultfile), os.path.join(
        app.config['USERS_FOLDER'], filename))
    return jsonify({"message": "success!"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7700)
