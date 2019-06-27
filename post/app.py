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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_extension(filename):
    return filename.rsplit('.', 1)[1]

def get_userid_for(postid):
    query="select userid from posts.post where postid='{0}'".format(postid)
    try:
        result=execute(query)
        return result[0][0]
    except:
        return None

def get_like_count(postid):
    query="select count(*) from posts.likes where postid='{0}'".format(postid)
    try:
        result=execute(query)
        return result[0][0]
    except:
        return None

def get_comment_count(postid):
    query="select count(*) from posts.comments where postid='{0}'".format(postid)
    try:
        result=execute(query)
        return result[0][0]
    except:
        return None

@app.route('/')
def hello():
    return jsonify({"message": "Hi,welcome to post server!"})

@app.route('/api/v1.0/getlikeslist/<postid>/<num>')
@token_required
def get_like_userids(userid,postid,num):
    #for first 20 likes num=0,for next 20 likes num=1 and so on...
    userid2=get_userid_for(postid)
    URL="http://localhost:7800/api/v1.0/followsornot/{0}/{1}".format(userid,userid2)
    r=requests.get(url=URL)
    result=r.json()
    if result["message"]=="false":
        return jsonify({"message":"error:not authorised"}),401
    base=10*int(num)
    top=base+10
    query="select userid from posts.likes where postid='{0}' order by date desc limit {1},{2}".format(postid,base,top)
    try:
        result=execute(query)
    except:
        return None
    likes=[]
    for like in result:
        liked={}
        liked["userid"]=like[0]
        likes.append(liked)
    return jsonify({"list":likes}),200

@app.route('/api/v1.0/getcommentslist/<postid>/<num>')
@token_required
def get_comments(userid,postid,num):
    #for first 20 comments num=0,for next 10 comments num=1 and so on...
    userid2=get_userid_for(postid)
    URL="http://localhost:7800/api/v1.0/followsornot/{0}/{1}".format(userid,userid2)
    r=requests.get(url=URL)
    result=r.json()
    if result["message"]=="false":
        return jsonify({"message":"error:not authorised"}),401
    base=20*int(num)
    top=base+20
    query="select * from posts.comments where postid='{0}' order by date desc limit {1},{2}".format(postid,base,top)
    try:
        result=execute(query)
    except:
        return None
    comments=[]
    for comment in result:
        commentd={}
        commentd["postid"]=comment[0]
        commentd["commentid"]=comment[1]
        commentd["userid"]=comment[2]
        commentd["date"]=comment[4]
        commentd["message"]=comment[5]
        comments.append(commentd)
    return jsonify({"list":comments}),200

@app.route('/api/v1.0/getpost/image/<postid>')
@token_required
def get_post(userid,postid):
    userid2=get_userid_for(postid)
    URL="http://localhost:7800/api/v1.0/followsornot/{0}/{1}".format(userid,userid2)
    r=requests.get(url=URL)
    result=r.json()
    data=[]
    if result["message"]=="false":
        query="select count(*) from posts.post where postid='{0}' and public=1".format(postid)
        result=execute(query)
        filename=os.path.join(app.config['POSTS_FOLDER'],postid+'.jpg')
        if result[0][0]==1:
            return send_file(filename,mimetype='image/gif')
        else:
            return jsonify({"message":"error:not authorised"}),401
    filename=os.path.join(app.config['POSTS_FOLDER'],postid+'.jpg')
    return send_file(filename,mimetype='image/gif')
    
    
@app.route('/api/v1.0/getpostsfor/user/<userid2>')
@token_required
def getpostfor(userid,userid2):
    URL="http://localhost:7800/api/v1.0/followsornot/{0}/{1}".format(userid,userid2)
    response=requests.get(url=URL)
    result=response.json()
    data=[]
    if result["message"]=="false":
        query="select * from posts.post where userid='{0}' and public='1'".format(userid2)
        try:    
            result=execute(query)
            for post in result:
                d={}
                userliked=execute("select count(*) from posts.likes where postid='{0}' and userid='{1}'".format(post[0],userid))[0][0]
                d["postid"]=post[0]
                d["userid"]=post[1]
                d["date"]=post[2]
                d["dateupdated"]=post[3]
                d["location"]=post[4]
                d["public"]=post[5]
                d["caption"]=post[6]
                d["likes"]=get_like_count(post[0])
                d["comments"]=get_comment_count(post[0])
                d["userliked"]=userliked
                data.append(d)
            return jsonify({"list":data}),200
        except:
            return jsonify({"message":"error"}),401
    query="select * from posts.post where userid='{0}'".format(userid2)
    try:    
        result=execute(query)
        for post in result:
            d={}
            d["postid"]=post[0]
            d["userid"]=post[1]
            d["date"]=post[2]
            d["dateupdated"]=post[3]
            d["location"]=post[4]
            d["public"]=post[5]
            d["caption"]=post[6]
            d["likes"]=get_like_count(post[0])
            d["comments"]=get_comment_count(post[0])
            data.append(d)
        return jsonify({"list":data}),200
    except:
        return jsonify({"message":"error"}),401


@app.route('/api/v1.0/delete/comment/<commentid>')
@token_required
def delete_comment(userid,commentid):
    query="delete from posts.comments where commentid='{0}' and userid='{1}'".format(commentid,userid)
    try:
        execute(query)
    except:
        return jsonify({"message":"error"}),401
    return jsonify({"message":"success!"}),200

@app.route('/api/v1.0/delete/like/<postid>')
@token_required
def delete_like(userid,postid):
    query="delete from posts.likes where postid='{0}' and userid='{1}'".format(postid,userid)
    try:
        execute(query)
    except:
        return jsonify({"message":"error"}),401
    return jsonify({"message":"success!"})

@app.route('/api/v1.0/comment/post/image/<postid>',methods=['GET','POST'])
@token_required
def commet_post(userid,postid):
    mainuser=get_userid_for(postid)
    if mainuser is None:
        return jsonify({"message":"error:post/user not found"}),401
    time=datetime.datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M:%S')
    data=request.get_json()
    if "comment" not in data:
        return jsonify({"message":"error:comment required"}),401
    comment=data["comment"]
    query="insert into posts.comments(postid,userid,mainuser,date,message) values('{0}','{1}','{2}','{3}','{4}')".format(postid,userid,mainuser,time,comment)
    try:
        execute(query)
        return jsonify({"message":"success"}),200
    except:
        return jsonify({"message":"error"}),401

@app.route('/api/v1.0/like/post/image/<postid>')
@token_required
def like_post(userid,postid):
    mainuser=get_userid_for(postid)
    if mainuser is None:
        return jsonify({"message":"error:post/user not found"}),401
    time=datetime.datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M:%S')
    likeid=userid+postid
    query="insert into posts.likes(likeid,postid,userid,mainuser,date) values('{0}','{1}','{2}','{3}','{4}')".format(likeid,postid,userid,mainuser,time)
    try:
        execute(query)
        return jsonify({"message":"success"}),200
    except:
        return jsonify({"message":"error"}),401

@app.route('/api/v1.0/update/post/image/<postid>', methods=['GET', 'POST'])
@token_required
def updatepost(userid, postid):
    if "file" not in request.files:
        return jsonify({"message": "error:file required"}), 401
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"message": "error:file required"}), 401
    if "details" not in request.form:
        return jsonify({"message": "error:details required"}), 401
    # Here details about post will be sent as form data("Content-Type:multipart/form-data")
    # The client must send details as form data where key is "details" and value is the whole json data(i.e. details of post)
    data = request.form["details"]
    data = json.loads(data)
    if "location" in data:
        location = data["location"]
    else:
        location = "null"
    if "public" in data:
        public = data["public"]
    else:
        public = "0"
    if "caption" in data:
        caption = data["caption"]
    else:
        caption = "null"
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    filename = str(postid)+'.jpg'
    os.remove(os.path.join(app.config['POSTS_FOLDER'], postid+".jpg"))
    if file and allowed_file(file.filename):
        if file_extension(file.filename) == "png":
            im = Image.open(request.files["file"].stream)
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(
                app.config['POSTS_FOLDER'], filename), "JPEG")
        else:
            file.save(os.path.join(app.config['POSTS_FOLDER'], filename))
        query = "update posts.post set dateupdated='{0}',location='{1}',public='{2}',caption='{3}' where userid='{4}' and postid='{5}'".format(
            time, location, public, caption, userid, postid)
        try:
            execute(query)
        except:
            return jsonify({"message": "error:unsuccessfull"}), 401

        return jsonify({"message": "success!", "postid": postid}), 200
    else:
        return jsonify({"message": "error:unsuccessfull"}), 401


@app.route('/api/v1.0/delete/post/image/<postid>')
@token_required
def deletepost(userid, postid):
    query = "delete from posts.post where userid='{0}' and postid='{1}'".format(
        userid, postid)
    try:
        execute(query)
        os.remove(os.path.join(app.config['POSTS_FOLDER'], postid+".jpg"))
    except:
        return jsonify({"message": "unsuccessfull"}), 401
    return jsonify({"message": "success!"})


@app.route('/api/v1.0/post/image', methods=['GET','POST'])
@token_required
def post(userid):
    if "file" not in request.files:
        return jsonify({"message": "error:file required"}), 401
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"message": "error:file required"}), 401
    if "details" not in request.form:
        return jsonify({"message": "error:details required"}), 401
    # Here details about post will be sent as form data("Content-Type:multipart/form-data")
    # The client must send details as form data where key is "details" and value is the whole json data(i.e. details of post)
    data = request.form["details"]
    data = json.loads(data)
    if "location" in data:
        location = data["location"]
    else:
        location = "null"
    if "public" in data:
        public = data["public"]
    else:
        public = "0"
    if "caption" in data:
        caption = data["caption"]
    else:
        caption = "null"
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    postid = uuid.uuid4()
    filename = str(postid)+'.jpg'

    if file and allowed_file(file.filename):
        if file_extension(file.filename) == "png":
            im = Image.open(request.files["file"].stream)
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(
                app.config['POSTS_FOLDER'], filename), "JPEG")
        else:
            file.save(os.path.join(app.config['POSTS_FOLDER'], filename))
        query = "insert into posts.post(postid,userid,date,dateupdated,location,public,caption) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(
            str(postid), userid, time, time, location, public, caption)
        try:
            execute(query)
        except:
            return jsonify({"message": "error:unsuccessfull"}), 401

        return jsonify({"message": "success!", "postid": postid}), 200
    else:
        return jsonify({"message": "error:unsuccessfull"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7900)
