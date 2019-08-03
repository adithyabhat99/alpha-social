from app import *

# search by name
@app.route('/search')
@token_required
def search(userid):
    num = request.args.get('num', default=0, type=int)
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    base = num*30
    top = base+30
    if firstname is not None and lastname is not None:
        query = "select userid,username from users.user where firstname='{0}' or firstname='{0}' and lastname='{1}' limit {2},{3}".format(
            firstname, lastname, base, top)
        data = []
        try:
            result = execute(query)
            for user in result:
                d = {}
                d["userid"] = user[0]
                d["username"] = user[1]
                data.append(d)
            return jsonify({"list": data}), 200
        except:
            return jsonify({"error": "could not fetch"}), 401
    elif firstname is not None and lastname is None:
        query = "select userid,username from users.user where firstname='{0}' limit {1},{2}".format(
            firstname, base, top)
        data = []
        try:
            result = execute(query)
            for user in result:
                d = {}
                d["userid"] = user[0]
                d["username"] = user[1]
                data.append(d)
            return jsonify({"list": data}), 200
        except:
            return jsonify({"error": "could not fetch"}), 401
    else:
        return jsonify({"message": "firstname or lastname required"}), 401