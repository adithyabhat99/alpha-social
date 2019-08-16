from flask import Flask, request, jsonify, make_response, send_file
from flaskext.mysql import MySQL
import uuid
import datetime
import jwt
import os
import shutil
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
mysql = MySQL(app)

app.secret_key = 'adi123secret'
app.config['API_SECRET_KEY'] = 'alphaapisecret'
# MySQL Configs
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 52000

mysql.init_app(app)


def execute(query):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except:
        raise


def get_userid(username):
    try:
        query = "select userid from users.user where username='{0}' or email='{0}' or phoneno='{0}'".format(
            username)
        data = execute(query)
        userid = data[0][0]
        return userid
    except:
        return None


def get_username(userid):
    try:
        query = "select username from users.user where userid='{0}'".format(
            userid)
        result = execute(query)
        return result[0][0]
    except:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"error": "token is missing"}), 401
        try:
            data = jwt.decode(token, app.secret_key)
        except:
            return jsonify({"error": "token is invalid"}), 401
        return f(data["userid"], *args, **kwargs)
    return decorated


@app.route('/devaccount',methods=['PUT'])
@token_required
def create_api_account(userid):
    appname = request.args.get('appname')
    query = "select count(*) from users.dev where devid='{0}'".format(
        userid)
    try:
        result = execute(query)
        if result[0] == 1:
            return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not create api account"}), 401

    query = "insert into users.dev(devid,appname) values('{0}','{1}')".format(
        userid, appname)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not create api account"}), 401


@app.route('/grantbasicaccess', methods=['PUT'])
@token_required
def givebasicaccess(userid):
    devid = request.args.get('devid')
    query = "select count(*) from users.dev where devid='{0}'".format(
        devid)
    try:
        result = execute(query)
        if result[0] != 1:
            return jsonify({"error": "dev not found"}), 401
    except:
        return jsonify({"error": "not found"}), 401
    query = "select count(*) from users.apiaccess where devid='{0}' and userid='{1}'".format(
        devid, userid)
    try:
        result = execute(query)
        if result[0][0] == 1:
            return jsonify({"message": "has access", "userid": userid}), 200
    except:
        return jsonify({"error": "could not give access"}), 401
    query = "insert into user.apiaccess(devid,userid) values('{0}','{1}')".format(
        devid, userid)
    try:
        execute(query)
        return jsonify({"message": "success", "userid": userid}), 200
    except:
        return jsonify({"error": "could not give access"}), 401


@app.route('/revokeaccess', methods=['DELETE'])
@token_required
def revokeaccess(userid):
    devid = request.args.get('devid')
    query = "delete from users.apiaccess where devid='{0}' and userid='{1}'".format(
        devid, userid)
    try:
        execute(query)
        return jsonify({"message": "success"}), 200
    except:
        return jsonify({"error": "could not revoke access"}), 401


@app.route('/details')
@token_required
def getdetails(userid):
    userid2 = request.args.get('userid')
    query = "select count(*) from users.dev where devid='{0}'".format(
        userid)
    try:
        result = execute(query)
        if result[0] != 1:
            return jsonify({"error": "dev not found"}), 401
    except:
        return jsonify({"error": "not found"}), 401
    query = "select count(*) from users.apiaccess where devid='{0}' and userid='{1}'".format(
        userid, userid2)
    try:
        result = execute(query)
        if result[0][0] != 1:
            return jsonify({"error": "not authorised"}), 401
    except:
        return jsonify({"error": "not authorised"}), 401

    query = "select * from users.user where userid='{0}'".format(userid2)
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
        details = {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phoneno": phoneno,
            "public": public,
            "datecreated": datecreated,
            "dateupdated": dateupdated,
            "bio": bio
        }
        return jsonify({"details": details}), 200
    except:
        return jsonify({"error": "could not fetch"}), 401


@app.route('/appname')
@token_required
def getappname_api(userid):
    devid = request.args.get('devid')
    query = "select appname from users.dev where devid='{0}'".format(devid)
    try:
        result = execute(query)
    except:
        return jsonify({"error": "could not get appname"}), 401
    return jsonify({"appname": result[0][0]}), 200


@app.route('/mydevs')
@token_required
def getmydevs(userid):
    query="select devid,appname from users.dev where userid='{0}'".format(userid)
    try:
        data=[]
        result=execute(query)
        for dev in result:
            d={}
            d["devid"]=dev[0]
            d["appname"]=dev[1]
            data.append(d)
        return jsonify({"list":data}),200
    except:
        return jsonify({"error":"coult not fetch devs"}),401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7750)
