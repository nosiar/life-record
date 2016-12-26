from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/a/")
def helloa():
    return "Hello World!a"

if __name__ == "__main__":
    app.run()
