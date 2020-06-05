# -*- encoding: utf-8 -*-
#
# config file for app
#
# 20-3-30 leo : Init

import os


class Config:
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'
    DATABASE_PORT = os.environ.get('DATABASE_PORT') or 3306
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASS = os.environ.get('DATABASE_PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_DATABASE = os.environ.get('DATABASE_DATABASE') or 'minus1_dev'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin123@localhost:3306/edge_computing"


class TestingConfig(Config):
    TESTING = True
    DATABASE_DATABASE = os.environ.get('DATABASE_DATABASE') or 'minus1_test'


class ProductionConfig(Config):
    DATABASE_DATABASE = os.environ.get('DATABASE_DATABASE') or 'minus1'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

