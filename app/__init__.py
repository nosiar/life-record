from flask import Flask
from .config import config
from .db import db
import os


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app

app = create_app(os.getenv('LIFE_CONFIG') or 'default')

from . import views
