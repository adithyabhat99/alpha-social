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


def Posts(query, userid):
    data=[]
    try:
        result = execute(query)
        for post in result:
            d = {}
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
            data.append(d)
        return jsonify({"list": data}), 200
    except:
        raise


@app.route('/')
def hello():
    return jsonify({"message": "Hi,welcome to home page server!"})

@app.route('/home')
@token_required
def home(userid):
    num = request.args.get('num', default=0, type=int)
    # num=0 for first 10 posts,num=1 for 10 to 20 and so on...
    URL = 'http://localhost/api/v1.0/f/followinglist?userid2={0}'.format(
        userid)
    response = requests.get(
        url=URL, headers={"x-access-token": request.headers["x-access-token"]})
    result = response.json()
    if "list" not in result:
        return jsonify({"message": "error"}), 401
    base = num*10
    top = base+10
    res = []
    for i in result["list"]:
        res.append(i["userid"])
    users = "','".join(map(str, res))
    users = "'"+users+"'"
    query = "select * from posts.post where userid in ('{0}',{1}) order by date desc limit {2},{3}".format(
        userid, users, base, top)
    try:
        return Posts(query,userid)
    except:
        return jsonify({"error": "could not fetch"}), 401


@app.route('/discover/latest')
@token_required
def discover(userid):
    num = request.args.get('num', default=0, type=int)
    base = num*10
    top = base+10
    query = "select * from posts.post where public=1 order by date desc limit {0},{1}".format(
        base, top)
    try:
        return Posts(query,userid)
    except:
        return jsonify({"error": "could not fetch"}), 401


@app.route('/discover/trending')
@token_required
def discover_trending(userid):
    num = request.args.get('num', default=0, type=int)
    base = num*10
    top = base+10
    query = "select postid from posts.likes where date(date)=curdate() group by postid order by count(*) limit {0},{1}".format(
        base, top)
    try:
        result = execute(query)
        res = []
        for postid in result:
            res.append(postid[0])
        ids = "','".join(map(str, res))
        ids = "'"+ids+"'"
        query = "select * from posts.post where public=1 and postid in({0})".format(
            ids)
        try:
            return Posts(query,userid)
        except:
            return jsonify({"error": "could not fetch"}), 401
    except:
        return jsonify({"error": "could not fetch"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)