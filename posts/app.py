from flask import Flask, request, jsonify, make_response, send_file, json
from flaskext.mysql import MySQL
import uuid
import datetime
import jwt
import os
import requests
import shutil
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from flask_cors import CORS, cross_origin
from aws import *

app = Flask(__name__)
mysql = MySQL(app)
CORS(app)

app.secret_key = 'adi123secret'
# MySQL Configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'posts'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 52100

mysql.init_app(app)

ALLOWED_EXTENSIONS = set(['jpg', 'png'])

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
            data = jwt.decode(token, app.secret_key)
        except:
            return jsonify({"error": "token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_userid_for(postid):
    query = "select userid from posts.post where postid='{0}'".format(postid)
    try:
        result = execute(query)
        return result[0][0]
    except:
        return None


def get_like_count(postid):
    query = "select count(*) from posts.likes where postid='{0}'".format(
        postid)
    try:
        result = execute(query)
        return result[0][0]
    except:
        return None


def get_comment_count(postid):
    query = "select count(*) from posts.comments where postid='{0}'".format(
        postid)
    try:
        result = execute(query)
        return result[0][0]
    except:
        return None


def postdetails(postid, userid):
    query = "select * from posts.post where postid='{0}'".format(postid)
    try:
        result = execute(query)
        d = {}
        for post in result:
            userliked = execute(
                "select count(*) from posts.likes where postid='{0}' and userid='{1}'".format(post[0], userid))[0][0]
            d["postid"] = post[0]
            d["userid"] = post[1]
            d["date"] = post[2]
            d["dateupdated"] = post[3]
            if post[4] == "Null":
                d["location"] = None
            else:
                d["location"] = post[4]
            d["public"] = post[5]
            if post[6] == "Null":
                d["caption"] = None
            else:
                d["caption"] = post[6]
            d["likes"] = get_like_count(post[0])
            d["comments"] = get_comment_count(post[0])
            d["userliked"] = userliked
        return {"data": d}
    except:
        return {"error": "could not get post details"}


def commentslist(postid, base, top):
    query = "select * from posts.comments where postid='{0}' order by date desc limit {1},{2}".format(
        postid, base, top)
    try:
        result = execute(query)
    except:
        return {"error": "could not fetch data"}
    comments = []
    header = request.headers
    for comment in result:
        commentd = {}
        commentd["postid"] = comment[0]
        commentd["commentid"] = comment[1]
        commentd["userid"] = comment[2]
        URL = "http://localhost/api/v1.0/a/getusername?userid2={0}".format(
            comment[2])
        try:
            r = requests.get(url=URL, headers=header)
            commentd["username"] = r.json()["username"]
        except:
            commentd["username"] = None
        commentd["date"] = comment[4]
        commentd["message"] = comment[5]
        comments.append(commentd)
    return {"list": comments}


def likeslist(postid,base,top,userid):
    query = "select userid from posts.likes where postid='{0}' order by date desc limit {1},{2}".format(
        postid, base, top)
    try:
        result = execute(query)
    except:
        return {"error": "could not fetch data"}
    likes = []
    header = request.headers
    for like in result:
        liked = {}
        liked["userid"] = like[0]
        try:
            URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
                userid, like[0])
            r = requests.get(url=URL)
            result = r.json()
        except:
            result = None
        if "message" in result and result["message"] == "true":
            liked["userfollows"] = True
        else:
            liked["userfollows"] = False
        URL = "http://localhost/api/v1.0/a/username?userid2={0}".format(
            like[0])
        try:
            r = requests.get(url=URL, headers=header)
            liked["username"] = r.json()["username"]
        except:
            raise
        likes.append(liked)
    return {"list": likes}

@app.route('/')
def hello():
    return jsonify({"message": "Hi,welcome to post server!"})

@app.route('/postdetails')
@token_required
def getpostdetails(userid):
    postid = request.args.get('postid')
    userid2 = get_userid_for(postid)

    # if post is public
    try:
        if execute("select count(*) from posts.post where postid='{0}' and public='1'".format(postid))[0][0] == 1:
            details = postdetails(postid, userid)
            if "error" in details:
                return jsonify({"error": details["error"]}), 401
            return jsonify(details), 200
    except:
        jsonify({"error": "could not fetch details"}), 401

    # otherwise
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    response = requests.get(url=URL)
    result = response.json()
    if result["message"] == "false":
        return jsonify({"error": "not authorised"}), 401
    details = postdetails(postid, userid)
    if "error" in details:
        return jsonify({"error": details["error"]}), 401
    return jsonify(details), 200


@app.route('/deleteallposts', methods=['DELETE'])
@token_required
def deleteallposts(userid):
    query = "select postid from posts.post where userid='{0}'".format(userid)
    try:
        result = execute(query)
        for post in result:
            delete_s3(post+'.jpg')
        query = "delete from posts.post where userid='{0}'".format(userid)
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not delete"}), 401

from post import *
from post_list import *
from like_comment import *
from aws import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7900)
