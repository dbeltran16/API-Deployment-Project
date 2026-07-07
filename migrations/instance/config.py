import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


def create_app(config_class=ProductionConfig):
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object(config_class)
    return app