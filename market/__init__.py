from flask import Flask
from market.models import db, User, Item
from market.routes import main
from market.init_data import add_initial_items, add_initial_users
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Set the SECRET_KEY from the .env file
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)  # Initialize db with the app

    # Create the database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")

    add_initial_users(app)
    add_initial_items(app)
    # Register the blueprint for routes
    app.register_blueprint(main)

    return app


app = create_app()
