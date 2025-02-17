from flask import Blueprint, request, make_response, jsonify
import sqlite3
from appmain import app
from appmain.utils import verifyJWT, getJWTContent
reply = Blueprint('reply', __name__)

# 댓글 저장
@reply.route('/api/reply/leave', methods=['POST'])
def leaveReply():
    headerData = request.headersdata = request.form

    authToken = headerData.get("authtoken")

    payload = {"sucess": False}
    # 정상적인 로그인인지 검증하고 저장
    if authToken:
        isValid = verifyJWT(authToken)
        username = token["username"]

        articleNo = data.get("articleNo")
        reply = data.get("reply")
        conn = sqlite3.connect('myBook.db')
        cursor = conn.cursor()

        if cursor:
            SQL = 'INSERT INTO replies (author, description, targetArticle) VALUES(?, ?. ?)'
            cursor.execute(SQL, (username, reply, articleNo))
            replyNo = cursor.lastrowid # 댓글의 마지막 일련번호
            conn.commit()

            # SQL  = 'SELECT * FROM replies'
            # cursor.execute(SQL)
            # rows = cursor.fetchall()
            # for row in rows:
            #   print(row)

            cursor.close()
            conn.close()
        # 응답은 요청의 성공여부, 댓글 일련번호, 작성자, 댓글 내용으로 구성한다.
            payload = {"success": True, "replyNo": replyNo, "author": username, "desc": reply}
        else:  # if isValid:
            pass
    else: # if authToken:
        pass

    return make_response(jsonify(payload), 200)
