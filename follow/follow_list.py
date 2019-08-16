from app import *

@app.route('/requestslist')
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

@app.route('/followinglist')
@token_required
def get_follower_list(userid):
    userid2 = request.args.get('userid2', default=userid)
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
        entry["userfollows"] = follows_or_not(userid, users[0])
        data.append(entry)
    return jsonify({"list": data}), 200


@app.route('/followerslist')
@token_required
# num=0 for first 10 followers num=1 for 10-20 and so on..
def get_follow_list(userid):
    userid2 = request.args.get('userid2', default=userid)
    num = request.args.get('num', default=0, type=int)
    if userid != userid2 and not follows_or_not(userid, userid2):
        return jsonify({"error": "not authorised"}), 401
    base = num*10
    top = base+10
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
        entry["userfollows"] = follows_or_not(userid, users[0])
        data.append(entry)
    return jsonify({"list": data}), 200
