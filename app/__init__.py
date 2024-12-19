from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
import urllib.parse
import os

# from .env file
config = dotenv_values(".env")

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    try:
        raw_password = config.get('DB_PASSWORD', '').strip('"').strip("'")
        password = urllib.parse.quote_plus(raw_password)

        # SQLAlchemy database URI using dotenv
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{config['DB_USER']}:{password}@"
            f"{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)

        with app.app_context():
            from . import routes
            app.register_blueprint(routes.routes)
            db.create_all()
            print("Database tables created successfully.")
    except KeyError as e:
        raise RuntimeError(f"Missing required environment variable: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize the application: {e}")

    return app
