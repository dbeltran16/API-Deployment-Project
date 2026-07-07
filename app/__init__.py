from app.config import ProductionConfig
from app.extensions import db, migrate


def create_app(config_class=ProductionConfig):
    from flask import Flask
    from app.routes import api

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so metadata is registered for Flask-Migrate autogenerate.
    from app import models  # noqa: F401

    app.register_blueprint(api)

    return app
