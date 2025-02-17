"""
작성자 : 김용현
작성일 : 2025.02.17
내용 : 상품 정보 저장을 위한 데이터 베이스 테이블 생성
"""
import sqlite3

conn = sqlite3.connect('myBook.db')
cursor = conn.cursor()

SQL = 'CREATE TABLE IF NOT EXISTS articles (articleNo INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT NOT NULL, title TEXT NOT NULL, category INTEGER, description TEXT, price INTEGER, picture TEXT)'

cursor.execute(SQL)

cursor.close()
conn.close()