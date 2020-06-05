# -*- encoding: utf-8 -*-
#
# init file for package app
#
# 20-3-30 leo : Init

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init modules
    db.init_app(app)

    # add blueprint
    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint, url_prefix='/books')

    return app
