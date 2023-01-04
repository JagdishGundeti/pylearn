import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    database="flask_db",
    user="root",
    password="",
    # charset="utf8mb4_general_ci",
    charset="utf8mb4",
    # cursorclass=pymysql.cusors.DictCursor
)

cursor = conn.cursor()
sql_query = """CREATE TABLE book(
    id integer PRIMARY KEY AUTO_INCREMENT,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""

cursor.execute(sql_query)
cursor.close()