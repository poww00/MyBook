from flask import Blueprint, request, make_response, jsonify
import sqlite3
from appmain import app
from appmain.utils import verifyJWT, getJWTContent
reply = Blueprint('reply', __name__)

# 댓글 저장
@reply.route('/api/reply/leave', methods=['POST'])
def leaveReply():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authtoken")

    payload = {"sucess": False}
    # 정상적인 로그인인지 검증하고 저장
    if authToken:
        isValid = verifyJWT(authToken)
        username = token["username"]

        if isValid:
            token = getJWTContent(authToken)
            usename = token["username"]

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

# 댓글을 읽어서 전달하는 함수
@reply.route('/api/reply/get', methods=['POST'])
def getReply():
    data = request.form
    articleNo = data["articleNo"]
    baseIndex = data["baseIndex"]
    numReplyRead = data["numReplyRead"]

    payload = {"success": False}

    try:
        conn = sqlite3.connect('myBook.db')
        cursor = conn.cursor()

        if cursor:
            SQL = 'SELECT replyNo, author, description from replies WHERE targetArtcle=? \ ORDER BY replyNo DESC LIMIT ?, ?'
            cursor.execute(SQL, (articleNo, baseIndex, numReplyRead))
            result = cursor.fetchall()

            SQL = 'SELECT COUNT(*) FROM replies WHERE targetArticle=?' 
            cursor.execute(SQL, (articleNo))
            numTotalReply = cursor.fetchone()[0]

            cursor.close()
        conn.close()

        replies={}
        for reply in result:
            replies.append({"replyNo": reply[0], "author": reply[1], "desc": reply[2]})
        # 전체 댓글 수보다 현재 읽은 댓글 수가 큰지, 작은지 확인
        if numTotalReply <= (int(baseIndex) + int(numReplyRead)):
            moreReplies = False
        else:
            moreReplies = True
        
        payload = {"success": True, "replies": replies, "moreReplies" : moreReplies}
    except Exception as err:
        print('[Error]getReply():%s' % err)

    return make_response(jsonify(payload), 200)

# 댓글 삭제
@reply.route('/api/reply/delete', methods=['POST'])
def deleteReply():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authtoken")

    payload = {"success": False}

    # 로그인 확인
    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            replyNo = data.get("replyNo")

            conn = sqlite3.connect('myBook.db')
            cursor = conn.cursor()
   
            if cursor:
                SQL = 'DELETE FROM replies WHERE replyNo= ?'
                cursor.execute(SQL, (replyNo))
                conn.commit()

            payload = {"success": True} 
        else: # if isValid:
            pass
    else:  # if authToken:
        pass

    return make_response(jsonify(payload), 200)
