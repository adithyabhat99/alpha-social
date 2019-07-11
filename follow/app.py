from flask import Flask, request, jsonify, make_response, send_file, json
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
mysql = MySQL(app)
CORS(app)

app.secret_key = 'adi123secret'
USERS_FOLDER = '/mnt/Users'
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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"error": "token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithm='SHA256')
        except:
            return jsonify({"error": "token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


def file_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_userid(username):
    try:
        query = "select userid from users.user where username='{0}'".format(
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
    except:
        return None
    try:
        username = result[0][0]
    except:
        return None
    return username


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


def public_or_not(userid):
    try:
        query = "select count(*) from users.user where userid='{0}' and public='1'".format(
            userid)
        result = execute(query)
        return result[0][0]
    except:
        return 0


@app.route('/')
def hi():
    return jsonify({"message": "hi! welcome to follow server"}), 200


@app.route('/follow/user', methods=['PUT'])
@token_required
def follow(userid):
    userid2 = request.args.get('userid2')
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    id = userid+'+'+userid2
    if public_or_not(userid2):
        try:
            query = "insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
                userid, userid2, time, id)
            execute(query)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not follow {0}".format(userid2)}), 401
    try:
        query = "insert into users.followre(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
            userid, userid2, time, id)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not follow {0}".format(userid2)}), 401


@app.route('/approve', methods=['PUT'])
@token_required
def approve(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.followre where follower='{0}' and followed='{1}'".format(
            userid2, userid)
        execute(query)
    except:
        return jsonify({"error": "could not approve {0}".format(userid2)}), 401
    try:
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        id = userid2+'+'+userid
        query = "insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
            userid2, userid, time, id)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not approve {0}".format(userid2)}), 401


@app.route('/getfollowerslist')
@token_required
# num=0 for first 20 followers num=1 for 20-40 and so on..
def get_follow_list(userid):
    userid2 = request.args.get('userid2')
    num = request.args.get('num', default=0, type=int)
    if userid != userid2 and not follows_or_not(userid, userid2):
        return jsonify({"error": "not authorised"}), 401
    base = num*20
    top = base+20
    query = "select follower from users.follow where followed='{0}' order by date desc limit {1},{2}".format(
        userid2, base, top)
    try:
        result = execute(query)
    except:
        return jsonify({"error": "could not fetch results"}), 401
    data = []
    for users in result:
        entry = {}
        entry["userid"] = users[0]
        entry["username"] = get_username(users[0])
        data.append(entry)
    return jsonify({"list": data}), 200


@app.route('/getfollowinglist')
@token_required
def get_follower_list(userid):
    userid2 = request.args.get('userid2')
    if userid != userid2 and not follows_or_not(userid, userid2):
        return jsonify({"error": "not authorised"}), 401
    query = "select followed from users.follow where follower='{0}' order by date".format(
        userid2)
    try:
        result = execute(query)
    except:
        return jsonify({"error": "could not fetch results"}), 401
    data = []
    for users in result:
        entry = {}
        entry["userid"] = users[0]
        entry["username"] = get_username(users[0])
        data.append(entry)
    return jsonify({"list": data}), 200


@app.route('/unfollow', methods=["DELETE"])
@token_required
def unfollow(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.follow where followed='{0}' and follower='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not unfollow"}), 401


@app.route('/disapprove', methods=['DELETE'])
@token_required
def disapprove(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.followre where follower='{0}' and followed='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not unfollow"}), 401


@app.route('/getrequestlist')
@token_required
def get_request_list(userid):
    try:
        query = "select * from users.followre where followed='{0}'".format(
            userid)
        result = execute(query)
        data = []
        for users in result:
            col = {}
            col["userid"] = users[0]
            col["username"] = get_username(users[0])
            data.append(col)
        return jsonify({"list": data}), 200
    except:
        return jsonify({"error": "could not fetch results"}), 401


@app.route('/removefollower', methods=['DELETE'])
@token_required
def removefollower(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.follow where follower='{0}' and following='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not remove follower"}), 401


@app.route('/muteuser', methods=['PUT'])
@token_required
def mute(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "update users.follow set muted='1' where follower='{0}' and following='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not mute"}), 401


@app.route('/reportuser', methods=['POST'])
@token_required
def report(userid):
    userid2 = request.args.get('userid2')
    try:
        query = " users.reports(userid,reportedby) values('{0}','{1}')".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not report"}), 401


@app.route("/suggestions/users")
@token_required
def suggestions(userid):
    num = request.args.get('num', default=0, type=int)
    base = 20*num
    top = base+10
    query = "select userid,username,firstname,lastname from users.user order by datecreated desc limit {0},{1}".format(
        base, top)
    try:
        result = execute(query)
        data = []
        for user in result:
            u = {}
            u["userid"] = user[0]
            u["username"] = user[1]
            u["firstname"] = user[2]
            u["lastname"] = user[3]
            data.append(u)
        return jsonify({"list": data}), 200
    except:
        jsonify({"error": "could not fetch"}), 401

# token not required
@app.route('/followsornot')
def follows_or_not_api():
    userid1 = request.args.get('userid1')
    userid2 = request.args.get('userid2')
    if follows_or_not(userid1, userid2):
        return jsonify({"message": "true"}), 200
    return jsonify({"message": "false"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7800)
