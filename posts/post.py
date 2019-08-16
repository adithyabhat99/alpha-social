from app import *
from aws import *

@app.route('/post')
@token_required
def get_post(userid):
    postid = request.args.get('postid')
    userid2 = get_userid_for(postid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    r = requests.get(url=URL)
    result = r.json()
    filename = postid+'.jpg'
    if result["message"] == "false":
        query = "select count(*) from posts.post where postid='{0}' and public=1".format(
            postid)
        result = execute(query)
        if result[0][0] == 1:
            download_s3(filename)
            return send_file('post.jpg', mimetype='image/gif')
        else:
            return jsonify({"error": "not authorised"}), 401
    download_s3(filename)
    return send_file('post.jpg', mimetype='image/gif')


@app.route('/post', methods=['POST'])
@token_required
def post(userid):
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 401
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "file required"}), 401
    if "details" not in request.form:
        return jsonify({"error": "details required"}), 401
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
            rgb_im.save(filename, "JPEG", dpi=(200, 200))
        else:
            im = Image.open(request.files["file"].stream)
            im.save(filename,"JPEG", dpi=(200, 200))
        query = "insert into posts.post(postid,userid,date,dateupdated,location,public,caption) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(
            str(postid), userid, time, time, location, public, caption)
        try:
            execute(query)
        except:
            return jsonify({"error": "unsuccessfull"}), 401
        try:
            upload_s3(filename)
            return jsonify({"message": "success!", "postid": postid}), 200
        except:
            return jsonify({"error": "unsuccessfull"}), 401
    else:
        return jsonify({"error": "only jpg and png files are supported"}), 401


@app.route('/post', methods=['PUT'])
@token_required
def updatepost(userid):
    postid = request.args.get('postid')
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 401
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "file required"}), 401
    if "details" not in request.form:
        return jsonify({"error": "details required"}), 401
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
            rgb_im.save(filename, "JPEG", dpi=(200, 200))
        else:
            im = Image.open(request.files["file"].stream)
            im.save(filename, dpi=(200, 200))
        query = "update posts.post set dateupdated='{0}',location='{1}',public='{2}',caption='{3}' where userid='{4}' and postid='{5}'".format(
            time, location, public, caption, userid, postid)
        try:
            execute(query)
        except:
            return jsonify({"error": "unsuccessfull"}), 401
        try:
            upload_s3(filename)
            return jsonify({"message": "success!", "postid": postid}), 200
        except:
            return jsonify({"error": "unsuccessfull"}), 401
    else:
        return jsonify({"error": "unsuccessfull"}), 401


@app.route('/post', methods=['DELETE'])
@token_required
def deletepost(userid):
    postid = request.args.get('postid')
    query = "delete from posts.post where userid='{0}' and postid='{1}'".format(
        userid, postid)
    try:
        execute(query)
    except:
        return jsonify({"error": "unsuccessfull"}), 401
    try:
        filename=postid+'jpg'
        delete_s3(filename)
    except:
        return jsonify({"error": "unsuccessfull"}), 401
    return jsonify({"message": "success!"}), 200
