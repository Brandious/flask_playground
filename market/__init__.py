from flask import Flask
from market.models import db
from market.routes import main
from market.init_data import add_initial_items

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)  # Initialize db with the app
    

     # Create the database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")
    
    add_initial_items(app)
     # Register the blueprint for routes
    app.register_blueprint(main)
    
        
    return app




app = create_app()

