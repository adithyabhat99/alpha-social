from app import *
from aws import *

@app.route('/myaccount', methods=['GET'])
@token_required
def getmydetails(userid):
    query = "select * from users.user where userid='{0}'".format(userid)
    try:
        result = execute(query)
        username = result[0][1]
        firstname = result[0][2]
        lastname = result[0][3]
        if result[0][7] == 1:
            if result[0][5][0] == "-":
                email = None
            else:
                email = result[0][5]
        else:
            # email = None if you add email verificaton feature
            if result[0][5][0] == "-":
                email = None
            else:
                email = result[0][5]
        if result[0][10] == 1:
            if result[0][8][0] == "-":
                phoneno = None
            else:
                phoneno = result[0][8]
        else:
            # phoneno = None if you add phone verification feature
            if result[0][8][0] == "-":
                phoneno = None
            else:
                phoneno = result[0][8]
        public = result[0][11]
        datecreated = result[0][12]
        dateupdated = result[0][13]
        if result[0][14] == 'Null':
            bio = None
        else:
            bio = result[0][14]
        followerscount = get_follow_count(userid)
        followingcount = get_following_count(userid)
        details = {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phoneno": phoneno,
            "public": public,
            "datecreated": datecreated,
            "dateupdated": dateupdated,
            "bio": bio,
            "followerscount": followerscount,
            "followingcount": followingcount
        }
        return jsonify({"details": details}), 200
    except:
        return jsonify({"error": "could not fetch"}), 401


@app.route('/myaccount', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify({"error": "data required"}), 401
    try:
        if 'username' in data:
            username = data['username']
            query = "select count(*) from users.user where username='{0}'".format(
                username)
            result = execute(query)
            if result[0][0] != 0:
                return jsonify({"error": "username already exists"}), 401
        else:
            return jsonify({"error": "username is must"}), 401
        userid = uuid.uuid4()
        if 'password' in data:
            hashed_password = generate_password_hash(
                data['password'], method='sha256')
        else:
            return jsonify({"error": "password is must"}), 401
        if 'firstname' in data:
            firstname = data['firstname']
        else:
            return jsonify({"error": "firstname is must"}), 401
        if 'lastname' in data:
            lastname = data['lastname']
        else:
            return jsonify({"error": "lastname is must"}), 401
        if 'bio' in data:
            bio = data['bio']
        else:
            bio = 'Null'
        if 'phoneno' not in data and 'email' not in data:
            return jsonify({"error": "email or phoneno is must"}), 401
        if 'phoneno' in data:
            if data['phoneno'] == "Null":
                phoneno = '-'+str(userid)[0:10]
            else:
                phoneno = data['phoneno']
        else:
            phoneno = '-'+str(userid)[0:10]
        if 'email' in data:
            if data['email'] == 'Null':
                email = '-'+str(userid)[0:10]
            else:
                email = data['email']
        else:
            email = '-'+str(userid)[0:10]
        if 'public' in data:
            public = data['public']
        else:
            public = '0'
        token = uuid.uuid4()
        phonetoken = uuid.uuid4()
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,bio) \
            values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}');".format(userid, username, firstname, lastname, hashed_password, email, phoneno,
                                                                                                              token, phonetoken, public, time, time, bio)
        execute(query)
        filename = str(userid)+".jpg"
        defaultfile = 'default.jpg'
        shutil.copy(defaultfile,filename)
        upload_s3(filename)
        token = jwt.encode({"userid": str(userid), "username": username, "exp": datetime.datetime.now(
        )+datetime.timedelta(days=7)}, app.secret_key)
        return jsonify({'x-access-token': token.decode('UTF-8'), 'userid': str(userid)}), 200
    except:
        jsonify({"error": "could not create account"}), 401


@app.route('/myaccount', methods=['DELETE'])
@token_required
def delte_account(userid):
    query = "delete from users.user where userid='{0}'".format(userid)
    os.remove(os.path.join(app.config['USERS_FOLDER'], userid+'.jpg'))
    URL = "http://localhost/api/v1.0/p/deleteallposts"
    try:
        execute(query)
        r = request.delete(url=URL, headers={
                           "x-access-token": request.headers["x-access-token"]})
        if r["message"] == "success":
            return jsonify({"message": "success"}), 200
        else:
            return jsonify({"error": "could not delete posts"}), 401
    except:
        return jsonify({"error": "could not delete"}), 401

# Update routes

@app.route('/update/password', methods=['PUT'])
@token_required
def update_password(userid):
    data = request.get_json()
    if not data or "old_password" not in data or "new_password" not in data:
        return jsonify({"error": "send old password and new password"}), 401
    query = "select password from users.user where userid='{0}'".format(userid)
    try:
        result = execute(query)
    except:
        return jsonify({"error": "could not update"}), 401
    if not check_password_hash(result[0][0], data["old_password"]):
        return jsonify({"error": "old password in incorrect"}), 401
    hashed_password = generate_password_hash(
        data["new_password"], method='SHA256')
    query = "update users.user set password='{0}' where userid='{1}'".format(
        hashed_password, userid)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not change password"}), 401


@app.route('/update/bio', methods=['PUT'])
@token_required
def update_bio(userid):
    data = request.get_json()
    if not data or "new_bio" not in data:
        return jsonify({"error": "data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set bio='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_bio'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/name', methods=['PUT'])
@token_required
def update_name(userid):
    data = request.get_json()
    if not data or "new_firstname" not in data or "new_lastname" not in data:
        return jsonify({"error": "data required"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set firstname='{0}',lastname='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_firstname'], data['new_lastname'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/phoneno', methods=['PUT'])
@token_required
def update_phone(userid):
    data = request.get_json()
    if not data or "new_phoneno" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where phoneno='{0}'".format(
        data['new_phoneno'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "phoneno already exists"}), 401
    except:
        return jsonify({"error": "error"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set phoneno='{0}',verified='0',phonetoken='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_phoneno'], uuid.uuid4(), time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "coul not update"}), 401


@app.route('/update/email', methods=['PUT'])
@token_required
def update_email(userid):
    data = request.get_json()
    if not data or "new_email" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where email='{0}'".format(
        data['new_email'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "email already exists"}), 401
    except:
        return jsonify({"error": "error"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set email='{0}',verified='0',token='{1}',dateupdated='{2}' where userid='{3}'".format(
        data['new_email'], uuid.uuid4(), time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401


@app.route('/update/public', methods=['PUT'])
@token_required
def update_public(userid):
    data = request.get_json()
    if not data or "public" not in data:
        return jsonify({"error": "data required"}), 401
    p = data["public"]
    query = "update users.user set public='{0}' where userid='{1}'".format(
        p, userid)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not update public"}), 401


@app.route('/update/username', methods=['PUT'])
@token_required
def updatedetails(userid):
    data = request.get_json()
    if not data or "new_username" not in data:
        return jsonify({"error": "data required"}), 401
    query = "select count(*) from users.user where username='{0}'".format(
        data['new_username'])
    try:
        result = execute(query)
        if result[0][0] != 0:
            return jsonify({"error": "username already exists"}), 401
    except:
        return jsonify({"error": "could not update"}), 401
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    query = "update users.user set username='{0}',dateupdated='{1}' where userid='{2}'".format(
        data['new_username'], time, userid)
    try:
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not update"}), 401