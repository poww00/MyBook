from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt
import secrets
import jwt

from appmain import app

from appmain.utils import verifyJWT, getJWTContent

user = Blueprint('user', __name__)

@user.route('/signup')
def signUp():
    return send_from_directory(app.root_path, 'templates/signup.html')

@user.route('/api/user/signup', methods=['POST'])
def register():
    data  = request.form
    
    username = data.get('username')
    email = data.get('email')
    passwd = data.get('passwd')

    hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('myBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'INSERT INTO users (username, email, passwd) VALUES (?, ?, ?)'
        cursor.execute(SQL, (username, email, hashedPW))
        conn.commit()

        SQL = 'SELECT * FROM users'
        cursor.execute(SQL)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
    conn.close()

    payload = {"success": True}
    return make_response(jsonify(payload), 200)

@user.route('/signin')
def signin():
    return send_from_directory(app.root_path, 'templates/signin.html')

@user.route('/api/user/signin', methods=['POST'])
def getAuth():

    data = request.form

    email = data.get("email")
    passwd = data.get("passwd")

    conn = sqlite3.connect('myBook.db')
    cursor = conn.cursor()

    payload = {"authenticated": False, "email": '', "username": "", "authtoken": ""}

    if cursor:
        SQL = 'SELECT id, username, passwd FROM users WHERE email=?'
        cursor.execute(SQL, (email,))
        result = cursor.fetchone()

        if result:
            pwMatch = bcrypt.checkpw(passwd.encode("utf-8"), result[2])
            id = result[0]
            username = result[1]
        else:
            pwMatch = None

        if pwMatch:
            authKey = secrets.token_hex(16)

            SQL = "UPDATE users SET authkey=? WHERE id=?"
            cursor.execute(SQL, (authKey, id))
            conn.commit()

            token = jwt.encode({"id": id, "email": email, "username": username, "authkey": authKey}
                               , app.config["SECRET_KEY"], algorithm='HS256')
            payload = {"authenticated": True, "email": email, "username": username, "authtoken": token}

        else:
            pass

        cursor.close()
    conn.close()

    return make_response(jsonify(payload), 200)

@user.route('/myinfo')
def myPage():
    return send_from_directory(app.root_path, 'templates/mypage.html')

@user.route('/api/user/myinfo', methods = ['POST'])
def getMyInfo():
    heanderDate = request.headers

    authToken = heanderDate.get("authtoken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)
        if isValid:
            token = getJWTContent(authToken)
            email = token['email']

            conn = sqlite3.connect('myBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'SELECT username FROM user WHERE email=?'
                cursor.execute(SQL, (email))
                username = cursor.fetchone()[0]
                cursor.close()
            conn.close()

            payload = {"success": True, "username": username}
    
    return make_response(jsonify(payload), 200)

@user.route('/api/user/update', methods = ['POST'])
def updateMyInfo():

    headerDate = request.headers
    data = request.form

    authToken = headerDate.get('authtoken')

    username = data.get("username")
    passwd = data.get("passwd")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)
        if isValid:
            token = getJWTContent(authToken)
            email = token["email"]

            hashedPW = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())

            conn = sqlite3.connect('myBook.db')
            cursor = conn.cursor()

            if cursor:
                if passwd:
                    SQL = "UPDATE users SET username=?, passwd=? WHERE email=?"
                    cursor.execute(SQL, (username, hashedPW, email))
                else:
                    SQL = "UPDATE users SET username=? WHERE email=?"
                    cursor.execute(SQL, (username, email))

                conn.commit()
                cursor.close()
            conn.close()
    
    return make_response(jsonify(payload), 200)

    