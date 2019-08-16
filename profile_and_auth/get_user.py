from app import *

@app.route('/details')
@token_required
def getdetails(userid):
    userid2 = request.args.get('userid2')
    query = "select firstname,lastname,bio,username from users.user where userid='{0}'".format(
        userid2)
    try:
        result = execute(query)
        firstname = result[0][0]
        lastname = result[0][1]
        if result[0][2] != "Null":
            bio = result[0][2]
        else:
            bio = None
        username2 = result[0][3]
    except:
        return jsonify({"error": "could not fetch details"}), 401
    followers = get_follow_count(userid2)
    following = get_following_count(userid2)
    data = {
        "username": username2,
        "userid": userid2,
        "firstname": firstname,
        "lastname": lastname,
        "bio": bio,
        "followerscount": followers,
        "followingcount": following,
        "userfollows": follows_or_not(userid, userid2)
    }
    return jsonify({"details": data}), 200

@app.route('/username')
@token_required
def get_username_api(userid):
    userid2 = request.args.get('userid2', default=userid)
    username = get_username(userid2)
    if username is None:
        return jsonify({"error": "could not get username"}), 401
    return jsonify({"username": username}), 200

@app.route('/userid')
@token_required
def get_userid_api(userid):
    username = request.args.get('username')
    userid2 = get_userid(username)
    username = get_username(userid)
    if userid is None:
        return jsonify({"error": "user not found"}), 401
    return jsonify({"userid": userid2, "username": username}), 200
