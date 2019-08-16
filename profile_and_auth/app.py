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
# MySQL Configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 52000

mysql.init_app(app)

ALLOWED_EXTENSIONS = set(['jpg', 'png'])

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
    query = "select count(*) from users.user where userid='{0}' and public='1'".format(
        userid2)
    result = execute(query)
    if result[0][0] == 1:
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


from myaccount import *
from search import *
from profilepic import *
from get_user import *
from aws import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7700)
