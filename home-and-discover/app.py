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

app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'adi123secret'
POSTS_FOLDER = '/mnt/Posts'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])
app.config['POSTS_FOLDER'] = POSTS_FOLDER
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
            return jsonify({"message": "error:token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithm='SHA256')
        except:
            return jsonify({"message": "error:token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


@app.route('/')
def hello():
    return jsonify({"message": "Hi,welcome to home page server!"})


@app.route('/api/v1.0/gethome')
@token_required
def home(userid):
    num = request.args.get('num', default=0, type=int)
    # num=0 for first 20 posts,num=1 for 20 to 40 and so on...
    URL = 'http://localhost:7800/api/v1.0/getfollowinglist?userid2={0}'.format(
        userid)
    response = requests.get(
        url=URL, headers={"x-access-token": request.headers["x-access-token"]})
    result = response.json()
    if "list" not in result:
        return jsonify({"message": "error"}), 401
    base = num*20
    top = base+20
    res = []
    for i in result["list"]:
        res.append(i["userid"])
    users = "','".join(map(str, res))
    users = "'"+users+"'"
    query = "select * from posts.post where userid in ({0}) order by date desc limit {1},{2}".format(
        users, base, top)
    result2 = execute(query)
    data = []
    for post in result2:
        d = {}
        try:
            userliked = execute(
                "select count(*) from posts.likes where postid='{0}' and userid='{1}'".format(post[0], userid))[0][0]
            d["postid"] = post[0]
            d["userid"] = post[1]
            d["date"] = post[2]
            d["dateupdated"] = post[3]
            d["location"] = post[4]
            d["public"] = post[5]
            d["caption"] = post[6]
            d["likes"] = get_like_count(post[0])
            d["comments"] = get_comment_count(post[0])
            d["userliked"] = userliked
            data.append(d)
        except:
            return jsonify({"message": "error"}), 401
    return jsonify({"list": data}), 200


@app.route('/api/v1.0/discover/latest')
@token_required
def discover(userid):
    num = request.args.get('num', default=0, type=int)
    base = num*20
    top = base+20
    query = "select * from posts.post where public=1 order by date desc limit {0},{1}".format(
        base, top)
    data = []
    try:
        result = execute(query)
        for post in result:
            d = {}
            d["postid"] = post[0]
            d["userid"] = post[1]
            d["date"] = post[2]
            d["dateupdated"] = post[3]
            d["location"] = post[4]
            d["public"] = post[5]
            d["caption"] = post[6]
            d["likes"] = get_like_count(post[0])
            d["comments"] = get_comment_count(post[0])
            data.append(d)
        return jsonify({"list": data}), 200
    except:
        return jsonify({"message": "error"}), 401


@app.route('/api/v1.0/discover/trending')
@token_required
def discover_trending(userid):
    num = request.args.get('num', default=0, type=int)
    base = num*20
    top = base+20
    query = "select postid from posts.likes where date(date)=curdate() order by count(*) desc limit {0},{1}".format(
        base, top)
    data = []
    try:
        result = execute(query)
        res = []
        for postid in result:
            res.append(postid[0])
        ids = "','".join(map(str, res))
        ids = "'"+ids+"'"
        query = "select * from posts.post where postid in({0})".format(ids)
        try:
            result = execute(query)
            for post in result:
                d = {}
                d["postid"] = post[0]
                d["userid"] = post[1]
                d["date"] = post[2]
                d["dateupdated"] = post[3]
                d["location"] = post[4]
                d["public"] = post[5]
                d["caption"] = post[6]
                d["likes"] = get_like_count(post[0])
                d["comments"] = get_comment_count(post[0])
                data.append(d)
            return jsonify({"list": data}), 200
        except:
            return jsonify({"message": "error"}), 401
    except:
        return jsonify({"message": "error"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)