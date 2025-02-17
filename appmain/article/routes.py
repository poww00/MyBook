from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3

from appmain import app
from appmain.utils import verifyJWT, getJWTContent, savePic

article = Blueprint('article',__name__)

@article.route('/create_article')
def createArticlePage():
    return send_from_directory(app.root_path, 'templates/create_article.html')

@article.route('/api/article/create', methods=['POST'])
def createArticle():
    headerData = request.headers
    data = request.form #HTTP 요청 본문 데이터 가져오기
    files = request.files # 업로드 파일 객체
    authToken = headerData.get('authtoken') # 사용자 인증 

    payload = {'success':False}
    
    if authToken:
        isValid = verifyJWT(authToken)
        if isValid:
            token = getJWTContent(authToken)
            username = token['username']
            category = data.get('category')
            title = data.get('title')
            desc = data.get('desc')
            price = data.get('price')

            if files:
                picFileName = savePic(files['picture'],username)

            # 업로드 데이터 파일 디버깅 코드
            # print('createArticle.username', username)
            # print('createArticle.category', category)
            # print('createArticle.title', title)
            # print('createArticle.desc', desc)

            conn = sqlite3.connect('myBook.db')
            cursor = conn.cursor()

            if cursor:
                if files:
                    SQL = 'INSERT INTO articles (author, title, category, description, price, picture)\Values(?,?,?,?,?,?)'
                    cursor.execute(SQL, (username, title,category,desc,price))
                    rowId = cursor.lastrowid
                    conn.commit()

                    # 동작 확인용 디버깅 코드
                    # SQL = 'SELECT * FROM articles'
                    # cursor.execute(SQL)
                    # rows = cursor.getchall()
                    # for row in rows:
                    #   print(row)

                cursor.close()
            conn.close()

            playload = {"success":True, "articleNo":rowId}
        else:
            pass
    else:
        pass
    return make_response(jsonify(payload), 200)