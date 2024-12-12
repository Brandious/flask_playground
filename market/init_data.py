from market.models import db
from market.models import Item

def add_initial_items(app):
    with app.app_context():
        # Drop all existing items
        try:
            db.session.query(Item).delete()
            db.session.commit()
            print("All existing items deleted!")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting items: {e}")
            return f"Error: {e}"
        # Check if items already exist to avoid duplicates
        if not Item.query.first():
            items = [
                Item(
                    name='Phone',
                    barcode='893212299897',
                    price=500,
                    description='A brand new phone'  # description is required based on your model
                ),
                Item(
                    name='Laptop',
                    barcode='123985473165',
                    price=900,
                    description='High performance laptop'
                ),
                Item(
                    name='Keyboard',
                    barcode='231985128446',
                    price=150,
                    description='Mechanical keyboard'
                )
            ]
            
            try:
                db.session.add_all(items)
                db.session.commit()
                print("Items added successfully!")
                return "Items added successfully!"
            except Exception as e:
                db.session.rollback()
                print(f"Error adding items: {e}")
                return f"Error: {e}"
        else:
            print("Items already exist in database")
            return "Items already exist in database"
