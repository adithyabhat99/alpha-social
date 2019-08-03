from app import *

# Like section

# old name like/post
@app.route('/like', methods=['PUT'])
@token_required
def like_post(userid):
    postid = request.args.get('postid')
    mainuser = get_userid_for(postid)
    if mainuser is None:
        return jsonify({"error": "post/user not found"}), 401
    userid2 = get_userid_for(postid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    response = requests.get(url=URL)
    result = response.json()
    if result["message"] == "false":
        return jsonify({"error": "not authorised"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    likeid = userid+postid
    query = "insert into posts.likes(likeid,postid,userid,mainuser,date) values('{0}','{1}','{2}','{3}','{4}')".format(
        likeid, postid, userid, mainuser, time)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not like"}), 401


# old name delete/like
@app.route('/like', methods=['DELETE'])
@token_required
def delete_like(userid):
    postid = request.args.get('postid')
    query = "delete from posts.likes where postid='{0}' and userid='{1}'".format(
        postid, userid)
    try:
        execute(query)
    except:
        return jsonify({"error": "could not delete"}), 401
    return jsonify({"message": "success!"}), 200


# Comment section 

@app.route('/comment', methods=['POST'])
@token_required
def commet_post(userid):
    postid = request.args.get('postid')
    data = request.get_json()
    mainuser = get_userid_for(postid)
    if mainuser is None:
        return jsonify({"error": "post/user not found"}), 401
    userid2 = get_userid_for(postid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    response = requests.get(url=URL)
    result = response.json()
    if result["message"] == "false":
        return jsonify({"error": "not authorised"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    if data is None:
        return jsonify({"error": "comment required"}), 401
    if 'comment' not in data:
        return jsonify({"error": "comment required"}), 401
    comment = data["comment"]
    if comment == "" or comment is None:
        return jsonify({"error": "empty comment not supported"}), 401
    query = "insert into posts.comments(postid,userid,mainuser,date,message) values('{0}','{1}','{2}','{3}','{4}')".format(
        postid, userid, mainuser, time, comment)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not post comment"}), 401


# old name delete/comment
@app.route('/comment', methods=['DELETE'])
@token_required
def delete_comment(userid):
    commentid = request.args.get('commentid')
    query = "delete from posts.comments where commentid='{0}' and userid='{1}'".format(
        commentid, userid)
    try:
        execute(query)
    except:
        return jsonify({"error": "could not delete"}), 401
    return jsonify({"message": "success!"}), 200