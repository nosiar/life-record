from flask import render_template
from . import app

@app.route('/')
def hello():
    return "Hello World! hoo"


@app.route('/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run()
