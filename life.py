from flask import Flask
from config import config
from db import db
import os


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app


def create_all():
    with app.app_context():
        db.create_all()

app = create_app(os.getenv('LIFE_CONFIG') or 'default')


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
