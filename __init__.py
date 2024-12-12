from flask import Flask
from .item import db, Item  # Now this import will work

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'

    
    db.init_app(app)
    
     # Create the database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")
        
        
    return app