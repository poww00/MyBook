import sqlite3

conn = sqlite3.connect('myBook.db')
cursor = conn.cursor()

# SQL = 'DROP TABLE replies'
###
# cursor.execute(SQL)

SQL = 'CREATE TABLE IF NOT EXISTS replies (replyNo INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT NOT NULL, description TEXT NOT NULL, targetArticle NOT NULL)'

cursor.execute(SQL)

cursor.close()
conn.close()