from app import *

@app.route('/userpostslist')
@token_required
def getpostfor(userid):
    num = request.args.get('num', default=0, type=int)
    userid2 = request.args.get('userid2', default=userid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    response = requests.get(url=URL)
    result = response.json()
    base = num*10
    top = base+10
    data = []
    if result["message"] == "false":
        query = "select * from posts.post where userid='{0}' and public='1' order by date desc limit {1},{2}".format(
            userid2, base, top)
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
            return jsonify({"error"""}), 401
    query = "select * from posts.post where userid='{0}' order by date desc limit {1},{2}".format(
        userid2, base, top)
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
        return jsonify({"error": "could not get posts"}), 401


@app.route('/likeslist')
@token_required
def get_like_userids(userid):
    postid = request.args.get('postid')
    num = request.args.get('num', default=0, type=int)
    # for first 10 likes num=0,for next 10 likes num=1 and so on...
    base = 10*num
    top = base+10
    try:
        if execute("select count(*) from posts.post where postid='{0}' and public='1'".format(postid))[0][0] == 1:
            details = likeslist(postid, base, top, userid)
            if "error" in details:
                return jsonify({"error": details["error"]}), 401
            return jsonify(details), 200
    except:
        jsonify({"error": "could not fetch details"}), 401
    userid2 = get_userid_for(postid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    r = requests.get(url=URL)
    result = r.json()
    if result["message"] == "false":
        return jsonify({"error": "not authorised"}), 401
    details = likeslist(postid, base, top, userid)
    if "error" in details:
        return jsonify({"error": details["error"]}), 401
    return jsonify(details), 200


@app.route('/commentslist')
@token_required
def get_comments(userid):
    postid = request.args.get('postid')
    num = request.args.get('num', default=0, type=int)
    # for first 10 comments num=0,for next 10 comments num=1 and so on...
    base = 10*num
    top = base+10
    try:
        if execute("select count(*) from posts.post where postid='{0}' and public='1'".format(postid))[0][0] == 1:
            details = commentslist(postid, base, top)
            if "error" in details:
                return jsonify({"error": details["error"]}), 401
            return jsonify(details), 200
    except:
        jsonify({"error": "could not fetch details"}), 401

    userid2 = get_userid_for(postid)
    URL = "http://localhost/api/v1.0/f/followsornot?userid1={0}&userid2={1}".format(
        userid, userid2)
    r = requests.get(url=URL)
    result = r.json()
    if result["message"] == "false":
        return jsonify({"error": "not authorised"}), 401
    details = commentslist(postid, base, top)
    if "error" in details:
        return jsonify({"error": details["error"]}), 401
    return jsonify(details), 200
