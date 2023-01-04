from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def db_connection():
    conn = False
    try:
        conn =pymysql.connect(
            host="127.0.0.1",
                database="flask_db",
                user="root",
                password="",
                # charset="utf8mb4_general_ci",
                charset="utf8mb4",
                # cursorclass=pymysql.cusors.DictCursor
                )
    except pymysql.Error as e:
        print(e)
    return conn
    

@app.route("/")
@app.route("/books",methods=['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book")
        books = [
            # dict(id=row["id"], author=row["author"], language=row["language"], title=row["title"])
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        if books is not None:
            return jsonify(books), 200
        else:
            return "No data found", 404

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book(author, language, title)
                    VALUES(%s, %s, %s)"""
        cursor.execute(sql,(new_author, new_lang, new_title))
        conn.commit()
        cursor.close()
        conn.close()
        return f"book with the id {cursor.lastrowid} created successfuly"
        # cursor.execute('SELECT last_insert_id()')
        # return f"book with the id {cursor.fetchone()} created successfuly"

@app.route("/books/<int:id>",methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id = %s",(id,))
        rows = cursor.fetchall()
        for row in rows:
            book = row
        cursor.close()
        conn.close()
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]

        updated_books = {
            "id":id,
            "author":author,
            "language":language,
            "title":title,
        }

        sql = """UPDATE book 
        SET
            author = %s,
            language = %s,
            title = %s
        WHERE
            id = %s
        """
        cursor = conn.cursor()
        rows = cursor.execute(sql,(author,language,title,id,))
        conn.commit()
        conn.close()
        return jsonify(updated_books), 200
    if request.method == 'DELETE':
        
        sql = """DELETE FROM book WHERE id = %s """
        cursor = conn.cursor()
        cursor.execute(sql,(id,))
        conn.commit()
        return f"book with the id {id} deleted successfuly"


if __name__ == "__main__":
    app.run(debug=True)
