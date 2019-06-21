from flask import Flask
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'adi'
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 52000
mysql.init_app(app)
@app.route('/')
def hello_world():
    query = "select * from users.user;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return 'done!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
