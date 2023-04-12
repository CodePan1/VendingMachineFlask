from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vending_machine.db"
    db.init_app(app)

    with app.app_context():
        from .routes import routes

        app.register_blueprint(routes)

        db.create_all()
        return app
