from app import *
from aws import *
import os

@app.route('/profilepic')
@token_required
def get_profile(userid):
    userid2 = request.args.get('userid2', default=userid)
    if userid2 is None:
        return jsonify({"error": "user not found"})
    filename = userid2+".jpg"
    download_s3(filename)
    return send_file("user.jpg", mimetype='image/gif'), 200


@app.route('/profilepic', methods=['POST'])
@token_required
def update(userid):
    if 'file' not in request.files:
        return jsonify({"error": "file required"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "file required"}), 401
    if file and allowed_file(file.filename):
        filename = str(userid)+'.jpg'
        if file_extension(file.filename) == "png":
            im = Image.open(request.files['file'].stream)
            rgb_im = im.convert('RGB')
            rgb_im.save(filename, "JPEG", dpi=(200, 200))
        else:
            im = Image.open(request.files["file"].stream)
            im.save(filename, "JPEG", dpi=(150, 150))
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M:%S')
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        try:
            execute(query)
        except:
            return jsonify({"error": "could not update"}), 401
        try:
            upload_s3(filename)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not update"}), 401
    else:
        return jsonify({"error": "only jpg and png files are supported"}), 401


@app.route('/profilepic', methods=['DELETE'])
@token_required
def delpic(userid):
    filename = userid+".jpg"
    defaultfile = 'defualt.jpg'
    shutil.copy(defaultfile, filename)
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = "update users.user set dateupdated='{0}' where userid='{1}'".format(
            time, userid)
        execute(query)
        try:
            upload_s3(filename)
            return jsonify({"message": "success!"}), 200
        except:
            return jsonify({"error": "could not delete"}), 401
    except:
        return jsonify({"error": "could not delete"}), 401