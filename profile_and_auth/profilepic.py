from app import *

# old name getprofilepic
@app.route('/profilepic')
@token_required
def get_profile(userid):
    userid2 = request.args.get('userid2', default=userid)
    if userid2 is None:
        return jsonify({"error": "user not found"})
    filename = os.path.join(app.config['USERS_FOLDER'], userid2+".jpg")
    return send_file(filename, mimetype='image/gif'), 200

# old name update/profilepic and it was a put method
@app.route('/profilepic', methods=['POST'])
@token_required
def update(userid):
    if 'file' not in request.files:
        return jsonify({"error": "file required"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "file required"}), 401
    if file and allowed_file(file.filename):
        os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
        filename = str(userid)+'.jpg'
        if file_extension(file.filename) == "png":
            im = Image.open(request.files['file'].stream)
            rgb_im = im.convert('RGB')
            rgb_im.save(os.path.join(
                app.config['USERS_FOLDER'], filename), "JPEG", dpi=(300, 300))
        else:
            im = Image.open(request.files["file"].stream)
            im.save(os.path.join(
                app.config['USERS_FOLDER'], filename), dpi=(300, 300))
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        try:
            execute(query)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not update"}), 401
    else:
        return jsonify({"error": "unsuccessfull"}), 401

# old name deleteprofilepic
@app.route('/profilepic', methods=['DELETE'])
@token_required
def delpic(userid):
    os.remove(os.path.join(app.config['USERS_FOLDER'], userid+".jpg"))
    filename = userid+".jpg"
    defaultfile = 'defualt.jpg'
    shutil.copy(os.path.join(app.config['USERS_FOLDER'], defaultfile), os.path.join(
        app.config['USERS_FOLDER'], filename))
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        execute(query)
        return jsonify({"message": "success!"}), 200
    except:
        return jsonify({"error": "could not delete"}), 401
