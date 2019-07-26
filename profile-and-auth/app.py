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
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
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


def execute(query):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except:
        raise


def get_userid(username):
    try:
        query = "select userid from users.user where username='{0}' or email='{0}' or phoneno='{0}'".format(
            username)
        data = execute(query)
        userid = data[0][0]
        return userid
    except:
        return None


def get_username(userid):
    try:
        query = "select username from users.user where userid='{0}'".format(
            userid)
        result = execute(query)
        return result[0][0]
    except:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"error": "token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key)
        except:
            return jsonify({"error": "token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_follow_count(userid):
    query = "select count(*) from users.follow where followed='{0}'".format(
        userid)
    try:
        result = execute(query)
        return result[0][0]
    except:
        return 0


def get_following_count(userid):
    query = "select count(*) from users.follow where follower='{0}'".format(
        userid)
    try:
        result = execute(query)
        return result[0][0]
    except:
        return 0


def follows_or_not(userid, userid2):
    if userid is None or userid2 is None:
        return False
    if userid == userid2:
        return True
    query = "select count(*) from users.follow where follower='{0}' and followed='{1}'".format(
        userid, userid2)
    result = execute(query)
    if result[0][0] == 0:
        return False
    return True


@app.route('/')
def hi():
    return jsonify({"message": "hi! welcome to profile server"}), 200


@app.route('/update/password', methods=['PUT'])
@token_required
def update_password(userid):
    data = request.get_json()
    if not data or "old_password" in data or "new_password" in data:
        return jsonify({"error": "send old password and new password"}), 401
    query = "select password from users.user where userid='{0}'".format(userid)
    try:
        result = execute(query)
    except:
        return jsonify({"error": "could not update"}), 401
    if not check_password_hash(result[0][0], data["old_password"]):
        return jsonify({"error": "old password in incorrect"}), 401
    hashed_password = generate_password_hash(
        data["new_password"], method='SHA256')
    query = "update users.user set password='{0}' where userid='{1}'".format(
        hashed_password, userid)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not change password"}), 401


@app.route('/update/bio', methods=['PUT'])
@token_required
def update_bio(userid):
    data = request.get_json()
    if not data or "new_bio" not in data:
        return jsonify({"error": "data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set bio='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_bio'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/name', methods=['PUT'])
@token_required
def update_name(userid):
    data = request.get_json()
    if not data or "new_firstname" not in data or "new_lastname" not in data:
        return jsonify({"error": "data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set firstname='{0}',lastname='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_firstname'], data['new_lastname'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/phoneno', methods=['PUT'])
@token_required
def update_phone(userid):
    data = request.get_json()
    if not data or "new_phoneno" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where phoneno='{0}'".format(
        data['new_phoneno'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "phoneno already exists"}), 401
    except:
        return jsonify({"error": "error"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set phoneno='{0}',verified='0',phonetoken='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_phoneno'], uuid.uuid4(), time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "coul not update"}), 401


@app.route('/update/email', methods=['PUT'])
@token_required
def update_email(userid):
    data = request.get_json()
    if not data or "new_email" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where email='{0}'".format(
        data['new_email'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "email already exists"}), 401
    except:
        return jsonify({"error": "error"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set email='{0}',verified='0',token='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_email'], uuid.uuid4(), time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/username', methods=['PUT'])
@token_required
def updatedetails(userid):
    data = request.get_json()
    if not data or "new_username" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where username='{0}'".format(
        data['new_username'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "username already exists"}), 401
    except:
        return jsonify({"error": "could not update"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set username='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_username'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/profilepic', methods=['PUT'])
@token_required
def update(userid):
    if 'file' not in request.files:
        return jsonify({"error": "file required"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "file required"}), 401
    if file and allowed_file(file.filename):
        os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
        filename = str(userid)+'.jpg'
        if file_extension(file.filename) == "png":
            im = Image.open(request.files['file'].stream)
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(
                app.config['USERS_FOLDER'], filename), "JPEG", dpi=(300, 300))
        else:
            im = Image.open(request.files["file"].stream)
            im.save(os.path.join(
                app.config['USERS_FOLDER'], filename), dpi=(300, 300))
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        try:
            execute(query)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not update"}), 401
    else:
        return jsonify({"error": "unsuccessfull"}), 401


@app.route('/deleteprofilepic', methods=['DELETE'])
@token_required
def delpic(userid):
    os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
    filename = userid+".jpg"
    defaultfile = 'defualt.jpg'
    shutil.copy(os.path.join(app.config['USERS_FOLDER'], defaultfile), os.path.join(
        app.config['USERS_FOLDER'], filename))
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not delete"}), 401


@app.route('/getmyprofilepic', methods=['GET'])
@token_required
def getmyprofilepic(userid):
    filename = os.path.join(app.config['USERS_FOLDER'], userid+".jpg")
    return send_file(filename, mimetype='image/gif')


@app.route('/getmydetails', methods=['GET'])
@token_required
def getmydetails(userid):
    query = "select * from users.user where userid='{0}'".format(userid)
    try:
        result = execute(query)
        username = result[0][1]
        firstname = result[0][2]
        lastname = result[0][3]
        if result[0][7] == 1:
            if result[0][5][0] == "-":
                email = None
            else:
                email = result[0][5]
        else:
            # email = None if you add email verificaton feature
            if result[0][5][0] == "-":
                email = None
            else:
                email = result[0][5]
        if result[0][10] == 1:
            if result[0][8][0] == "-":
                phoneno = None
            else:
                phoneno = result[0][8]
        else:
            # phoneno = None if you add phone verification feature
            if result[0][8][0] == "-":
                phoneno = None
            else:
                phoneno = result[0][8]
        public = result[0][11]
        datecreated = result[0][12]
        dateupdated = result[0][13]
        if result[0][14] == 'Null':
            bio = None
        else:
            bio = result[0][14]
        followerscount = get_follow_count(userid)
        followingcount = get_following_count(userid)
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
            "followerscount": followerscount,
            "followingcount": followingcount
        }
        return jsonify({"details": details}), 200
    except:
        return jsonify({"error": "could not fetch"}), 401


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"error": "could not verify 1"}), 401
    query = "select count(*) from users.user where username='{0}' or email='{1}' or phoneno='{2}'".format(
        auth.username, auth.username, auth.username)
    try:
        result = execute(query)
        if result[0][0] != 1:
            return jsonify({"error": "could not verify 2"}), 401
        query = "select userid,password from users.user where username='{0}' or email='{0}' or phoneno='{0}'".format(
            auth.username)
        result = execute(query)
        userid = result[0][0]
        password = result[0][1]
        if check_password_hash(password, auth.password):
            token = jwt.encode({"userid": result[0][0], "username": auth.username, "exp": datetime.datetime.now(
            )+datetime.timedelta(days=7)}, app.secret_key)
            return jsonify({'x-access-token': token.decode('UTF-8'), 'userid': userid}), 200
        return jsonify({"error": "could not verify 3"}), 401
    except:
        return jsonify({"error": "could not verify 4"}), 401


@app.route('/createaccount', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({"error": "data required"}), 401
    try:
        if 'username' in data:
            username = data['username']
            query = "select count(*) from users.user where username='{0}'".format(
                username)
            result = execute(query)
            if result[0][0] != 0:
                return jsonify({"error": "username already exists"}), 401
        else:
            return jsonify({"error": "username is must"}), 401
        userid = uuid.uuid4()
        if 'password' in data:
            hashed_password = generate_password_hash(
                data['password'], method='sha256')
        else:
            return jsonify({"error": "password is must"}), 401
        if 'firstname' in data:
            firstname = data['firstname']
        else:
            return jsonify({"error": "firstname is must"}), 401
        if 'lastname' in data:
            lastname = data['lastname']
        else:
            return jsonify({"error": "lastname is must"}), 401
        if 'bio' in data:
            bio = data['bio']
        else:
            bio = 'null'
        if 'phoneno' not in data and 'email' not in data:
            return jsonify({"error": "email or phoneno is must"}), 401
        if 'phoneno' in data:
            if data['phoneno'] == "Null":
                phoneno = '-'+str(userid)[0:10]
            else:
                phoneno = data['phoneno']
        else:
            phoneno = '-'+str(userid)[0:10]
        if 'email' in data:
            if data['email'] == 'Null':
                email = '-'+str(userid)[0:10]
            else:
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
        execute(query)
        filename = str(userid)+".jpg"
        defaultfile = 'defualt.jpg'
        shutil.copy(os.path.join(app.config['USERS_FOLDER'], defaultfile), os.path.join(
            app.config['USERS_FOLDER'], filename))
        token = jwt.encode({"userid": str(userid), "username": username, "exp": datetime.datetime.now(
        )+datetime.timedelta(days=7)}, app.secret_key)
        return jsonify({'x-access-token': token.decode('UTF-8'), 'userid': str(userid)}), 200
    except:
        raise


@app.route('/getdetails')
@token_required
def getdetails(userid):
    userid2 = request.args.get('userid2')
    query = "select firstname,lastname,bio,username from users.user where userid='{0}'".format(
        userid2)
    try:
        result = execute(query)
        firstname = result[0][0]
        lastname = result[0][1]
        if result[0][2] != "Null":
            bio = result[0][2]
        else:
            bio = None
        username2 = result[0][3]
    except:
        return jsonify({"error": "could not fetch details"}), 401
    followers = get_follow_count(userid2)
    following = get_following_count(userid2)
    data = {
        "username": username2,
        "userid": userid2,
        "firstname": firstname,
        "lastname": lastname,
        "bio": bio,
        "followerscount": followers,
        "followingcount": following,
        "userfollows": follows_or_not(userid2)
    }
    return jsonify({"details": data}), 200


@app.route('/getprofilepic')
@token_required
def get_profile(userid):
    userid2 = request.args.get('userid2', default=userid)
    if userid2 is None:
        return jsonify({"error": "user not found"})
    filename = os.path.join(app.config['USERS_FOLDER'], userid2+".jpg")
    return send_file(filename, mimetype='image/gif'), 200


@app.route('/getusername')
@token_required
def get_username_api(userid):
    userid2 = request.args.get('userid2', default=userid)
    username = get_username(userid2)
    if username is None:
        return jsonify({"error": "could not get username"}), 401
    return jsonify({"username": username}), 200


@app.route('/getuserid')
@token_required
def get_userid_api(userid):
    username = request.args.get('username')
    userid2 = get_userid(username)
    username = get_username(userid)
    if userid is None:
        return jsonify({"error": "user not found"}), 401
    return jsonify({"userid": userid2, "username": username}), 200


@app.route('/deletemyaccount', methods=['DELETE'])
@token_required
def delte_account(userid):
    query = "delete from users.user where userid='{0}'".format(userid)
    os.remove(os.path.join(app.config['USERS_FOLDER'], userid+'.jpg'))
    URL = "http://localhost/api/v1.0/p/deleteallposts"
    try:
        execute(query)
        r = request.delete(url=URL, headers={
                           "x-access-token": request.headers["x-access-token"]})
        if r["message"] == "success":
            return jsonify({"message": "success"}), 200
        else:
            return jsonify({"error": "could not delete posts"}), 401
    except:
        return jsonify({"error": "could not delete"}), 401


# search by name
@app.route('/search')
@token_required
def search():
    num = request.args.get('num', default=0, type=int)
    firstname = request.args.get('firstname', defualt=None, trype=str)
    lastname = request.args.get('lastname', default=None, type=str)
    base = num*30
    top = base+30
    if firstname is not None and lastname is not None:
        query = "select userid,username from users.user where firstname'{0}' or firstname='{0}' and lastname='{1}' limit {2},{3}".format(
            firstname, lastname, base, top)
        data = []
        try:
            result = execute(query)
            for user in result:
                d = {}
                d["userid"] = user[0]
                d["username"] = user[1]
                data.append(d)
            return jsonify({"list": data}), 200
        except:
            return jsonify({"error": "could not fetch"}), 401
    elif firstname is not None and lastname is None:
        query = "select userid,username from users.user where firstname'{0}' limit {1},{2}".format(
            firstname, base, top)
        data = []
        try:
            result = execute(query)
            for user in result:
                d = {}
                d["userid"] = user[0]
                d["username"] = user[1]
                data.append(d)
            return jsonify({"list": data}), 200
        except:
            return jsonify({"error": "could not fetch"}), 401
    else:
        return jsonify({"message": "username or name required"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7700)
