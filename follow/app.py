from flask import Flask, request, jsonify, make_response, send_file,json
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
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
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
            return jsonify({"message": "error:token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithm='SHA256')
        except:
            return jsonify({"message": "error:token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated

def file_extension(filename):
    return filename.rsplit('.', 1)[1]

def get_userid(username):
    try:
        query="select userid from users.user where username='{0}'".format(username)
        data=execute(query)
        userid=data[0][0]
        return userid
    except:
        return None

def get_username(userid):
    try:
        query="select username from users.user where userid='{0}'".format(userid)
        result=execute(query)
    except:
        return None
    try:
        username=result[0][0]
    except:
        return None
    return username

def follows_or_not(userid,userid2):
    if userid is None or userid2 is None:
        return False
    if userid==userid2:
        return True
    query="select count(*) from users.follow where follower='{0}' and followed='{1}'".format(userid,userid2)
    result=execute(query)
    if result[0][0]==0:
        return False
    return True

def get_follow_count(userid):
    query="select count(*) from users.follow where followed='{0}'".format(userid)
    try:
        result=execute(query)
        return result[0][0]
    except:
        return 0


def get_following_count(userid):
    query="select count(*) from users.follow where follower='{0}'".format(userid)
    try:
        result=execute(query)
        return result[0][0]
    except:
        return 0

def public_or_not(userid):
    try:
        query="select count(*) from users.user where userid='{0}' and public='1'".format(userid)
        result=execute(query)
        return result[0][0]
    except:
        return 0

@app.route('/')
def hi():
    return jsonify({"mesage": "hi! welcome to follow server"}), 200

@app.route('/api/v1.0/follow/user/<userid2>')
@token_required
def follow(userid,userid2):
    time=datetime.datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M:%S')
    id=userid+'+'+userid2
    if public_or_not(userid2):
        try:
            query="insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(userid,userid2,time,id)
            execute(query)
            return jsonify({"message":"success!"}),200
        except:
            return jsonify({"message":"error:could not follow {0}".format(userid2)}),401
    try:
        query="insert into users.followre(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(userid,userid2,time,id)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not follow {0}".format(userid2)}),401

@app.route('/api/v1.0/follow/approve/<userid2>',methods=['GET','POST'])
@token_required
def approve(userid,userid2):
    try:
        query="delete from users.followre where follower='{0}' and followed='{1}'".format(userid2,userid)
        execute(query)
    except:
        return jsonify({"message":"error:could not approve {0}".format(userid2)}),401
    try:
        time=datetime.datetime.now()
        time=time.strftime('%Y-%m-%d %H:%M:%S')
        id=userid2+'+'+userid
        query="insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(userid2,userid,time,id)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not approve {0}".format(userid2)}),401

@app.route('/api/v1.0/getfollowerslist/<userid2>/<num>')
@token_required
#num=0 for first 20 followers num=1 for 20-40 and so on..
def get_follow_list(userid,userid2,num):
    if userid!=userid2 and not follows_or_not(userid,userid2):
        return jsonify({"message":"error:not authorised"}),401
    base=int(num)*20
    top=base+20
    query="select follower from users.follow where followed='{0}' order by date desc limit {1},{2}".format(userid2,base,top)
    try:
        result=execute(query)
    except:
        return jsonify({"message":"error:could not fetch results"}),401
    data=[]
    for users in result:
        entry={}
        entry["userid"]=users[0]
        entry["username"]=get_username(users[0])
        data.append(entry)
    return jsonify({"list":data}),200

@app.route('/api/v1.0/getfollowinglist/<userid2>')
@token_required
def get_follower_list(userid,userid2):
    if userid!=userid2 and not follows_or_not(userid,userid2):
        return jsonify({"message":"error:not authorised"}),401
    query="select followed from users.follow where follower='{0}' order by date".format(userid2)
    try:
        result=execute(query)
    except:
        return jsonify({"message":"error:could not fetch results"}),401
    data=[]
    for users in result:
        entry={}
        entry["userid"]=users[0]
        entry["username"]=get_username(users[0])
        data.append(entry)
    return jsonify({"list":data}),200

@app.route('/api/v1.0/unfollow/<userid2>')
@token_required
def unfollow(userid,userid2):
    try:
        query="delete from users.follow where followed='{0}' and follower='{1}'".format(userid2,userid)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not unfollow"}),401

@app.route('/api/v1.0/disapprove/<userid2>')
@token_required
def disapprove(userid,userid2):
    try:
        query="delete from users.followre where follower='{0}' and followed='{1}'".format(userid2,userid)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not unfollow"}),401

@app.route('/api/v1.0/getrequestlist')
@token_required
def get_request_list(userid):
    try:
        query="select * from users.followre where followed='{0}'".format(userid)
        result=execute(query)
        data=[]
        for users in result:
            col={}
            col["userid"]=users[0]
            col["username"]=get_username(users[0])
            data.append(col)
        return jsonify({"list":data}),200
    except:
        return jsonify({"message":"error:could not fetch results"}),401

@app.route('/api/v1.0/removefollower/<userid2>')
@token_required
def removefollower(userid,userid2):
    try:
        query="delete from users.follow where follower='{0}' and following='{1}'".format(userid2,userid)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not remove follower"}),401

@app.route('/api/v1.0/muteuser/<userid2>')
@token_required
def mute(userid,userid2):
    try:
        query="update users.follow set muted='1' where follower='{0}' and following='{1}'".format(userid2,userid)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not mute"}),401

@app.route('/api/v1.0/reportuser/<userid2>')
@token_required
def report(userid,userid2):
    try:
        query=" users.reports(userid,reportedby) values('{0}','{1}')".format(userid2,userid)
        execute(query)
        return jsonify({"message":"success!"}),200
    except:
        return jsonify({"message":"error:could not report"}),401

#token not required
@app.route('/api/v1.0/getdetails/<userid2>')
def getdetails(userid2):
    query="select firstname,lastname,bio,username from users.user where userid='{0}'".format(userid2)
    try:
        result=execute(query)
        firstname=result[0][0]
        lastname=result[0][1]
        bio=result[0][2]
        username2=result[0][3]
    except:
        return jsonify({"message":"error:could not fetch details"}),401
    followers=get_follow_count(userid2)
    following=get_following_count(userid2)
    data={
        "username":username2,
        "userid":userid2,
        "firstname":firstname,
        "lastname":lastname,
        "bio":bio,
        "followerscount":followers,
        "followingcount":following
    }
    return jsonify(data),200

#token not required
@app.route('/api/v1.0/getprofilepic/<userid2>')
def get_profile(userid2):
    if userid2 is None:
        return jsonify({"message":"error:user not found"})
    filename = os.path.join(app.config['USERS_FOLDER'], userid2+".jpg")
    return send_file(filename, mimetype='image/gif'),200

#token not required
@app.route('/api/v1.0/getusername/<userid>')
def get_username_api(userid):
    try:
        query="select username from users.user where userid='{0}'".format(userid)
        result=execute(query)
    except:
        return jsonify({"message":"error"}),401
    try:
        username=result[0][0]
    except:
        return jsonify({"message":"error:user not found"}),401
    return jsonify({"userid":userid,"username":username}),200

#token not required
@app.route('/api/v1.0/getuserid/<username>')
def get_userid_api(username):
    userid=get_userid(username)
    if userid is None:
        return jsonify({"message":"error:user not found"}),401
    return jsonify({"userid":userid,"username":username}),200

# Do for get userids for name,username etc.

#token not required
@app.route('/api/v1.0/followsornot/<userid1>/<userid2>')
def follows_or_not_api(userid1,userid2):
    if follows_or_not(userid1,userid2):
        return jsonify({"message":"true"}),200
    return jsonify({"message":"false"}),200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7800)