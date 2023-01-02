from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    user_agent = request.headers.get('User-Agent')
    return f"Your browser is {user_agent}"
    # return "Hello World"

@app.route("/<name>")
def print_name(name):
    name = "hi {},".format(name)
    return name

# http://127.0.0.1:5000/api/foo/?a=hello&b=world
@app.route('/api/foo/', methods=['GET'])
def foo():
    bar = request.args.to_dict()
    return bar, 200

if __name__ == "__main__":
    app.run(debug=True)
