from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = False
    try:
        conn =sqlite3.connect("books.sqlite")
    except sqlite3.Error as e:
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
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books), 200
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book(author, language, title)
                    VALUES(?, ?, ?)"""
        cursor = conn.execute(sql,(new_author, new_lang, new_title))
        conn.commit()
        return f"book with the id {cursor.lastrowid} created successfuly"

@app.route("/books/<int:id>",methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        rows = cursor.execute("SELECT * FROM book WHERE id = ?",(id,))
        for r in rows:
            book = r
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
            author = ?,
            language = ?,
            title = ?
        WHERE
            id = ?
        """
        rows = conn.execute(sql,(author,language,title,id,))
        conn.commit()
        return jsonify(updated_books), 200
    if request.method == 'DELETE':
        
        sql = """DELETE FROM book WHERE id = ? """
        rows = conn.execute(sql,(id,))
        conn.commit()
        return f"book with the id {id} deleted successfuly"


if __name__ == "__main__":
    app.run(debug=True)
