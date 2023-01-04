from flask import Flask, request, jsonify
app = Flask(__name__)

books_list = [
  {
    "id": "1",
    "author": "Chinua Achebe",
    "language": "English",
    "title": "Things Fall Apart",
  },
  {
    "id": "2",
    "author": "Hans Christian Andersen",
    "language": "Danish",
    "title": "Fairy tales",
  },
  {
    "id": "3",
    "author": "Dante Alighieri",
    "language": "Italian",
    "title": "The Divine Comedy",
  },
]

@app.route("/")
@app.route("/books",methods=['GET','POST'])
def books():
    if request.method == 'GET':
        if len(books_list):
            return jsonify(books_list)
        else:
            return "Nothing is found", 404
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        num = int(books_list[-1]['id'])+1
        id = str(num)
        new_obj ={
            "id": id,
            "author": new_author,
            "language": new_lang,
            "title": new_title,
        }
        books_list.append(new_obj)
        return jsonify(books_list),201

@app.route("/books/<int:id>",methods=['GET','PUT','DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if int(book["id"]) == id:
                return jsonify(book)
            pass
    if request.method == 'PUT':
        for book in books_list:
            if int(book["id"]) == id:
                book["author"] = request.form["author"]
                book["language"] = request.form["language"]
                book["title"] = request.form["title"]
                updated_book = [
                    book["author"],
                    book["language"],
                    book["title"],
                    book["id"],
                ]
                return jsonify(updated_book)
    if request.method == 'DELETE':
        for book in books_list:
            if int(book["id"]) == id:
                books_list.remove(book)
        return jsonify(books_list)


if __name__ == "__main__":
    app.run(debug=True)
