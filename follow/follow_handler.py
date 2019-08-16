from app import *

@app.route('/follow', methods=['PUT'])
@token_required
def follow(userid):
    userid2 = request.args.get('userid2')
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    Id = userid+'+'+userid2
    if public_or_not(userid2):
        try:
            query = "insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
                userid, userid2, time, Id)
            execute(query)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not follow {0}".format(userid2)}), 401
    try:
        query = "insert into users.followre(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
            userid, userid2, time, Id)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not follow {0}".format(userid2)}), 401


@app.route('/approve', methods=['PUT'])
@token_required
def approve(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.followre where follower='{0}' and followed='{1}'".format(
            userid2, userid)
        execute(query)
    except:
        return jsonify({"error": "could not approve {0}".format(userid2)}), 401
    try:
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        id = userid2+'+'+userid
        query = "insert into users.follow(follower,followed,date,id) values('{0}','{1}','{2}','{3}')".format(
            userid2, userid, time, id)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not approve {0}".format(userid2)}), 401



@app.route('/disapprove', methods=['DELETE'])
@token_required
def disapprove(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.followre where follower='{0}' and followed='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not unfollow"}), 401


@app.route('/unfollow', methods=["DELETE"])
@token_required
def unfollow(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.follow where followed='{0}' and follower='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not unfollow"}), 401


@app.route('/removefollower', methods=['DELETE'])
@token_required
def removefollower(userid):
    userid2 = request.args.get('userid2')
    try:
        query = "delete from users.follow where follower='{0}' and following='{1}'".format(
            userid2, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not remove follower"}), 401
