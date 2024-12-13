from market.models import db
from market.models import Item, User
import random
import string
import bcrypt


product_names = [
    "Apple iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "OnePlus 9", "Sony WH-1000XM4",
    "Apple MacBook Pro 16", "Dell XPS 13", "HP Spectre x360", "Lenovo ThinkPad X1 Carbon", "Microsoft Surface Pro 7",
    "Apple iPad Air", "Samsung Galaxy Tab S7", "Amazon Fire HD 10", "Fitbit Charge 5", "Garmin Forerunner 245",
    "Bose QuietComfort 35 II", "JBL Flip 5", "Logitech G502 Hero", "Razer DeathAdder V2", "Corsair K95 RGB",
    "ASUS ROG Strix Scar 15", "Acer Predator Helios 300", "MSI GS66 Stealth", "NVIDIA GeForce RTX 3080", "AMD Ryzen 9 5900X",
    "Seagate Expansion Portable 2TB", "WD My Passport 4TB", "Samsung T7 Portable SSD", "SanDisk Extreme Pro USB", "TP-Link Archer AX6000",
    "Netgear Nighthawk M1", "Google Nest Hub", "Amazon Echo Dot (4th Gen)", "Apple HomePod Mini", "Philips Hue White and Color",
    "Oculus Quest 2", "DJI Mavic Air 2", "GoPro HERO9 Black", "Canon EOS R5", "Nikon Z6 II",
    "Sony A7 III", "Panasonic Lumix GH5", "BenQ PD3220U", "LG UltraFine 5K", "Dell UltraSharp U2720Q",
    "ViewSonic XG2405", "Epson Home Cinema 2150", "Anker PowerCore 26800", "RAVPower 20000mAh", "Apple AirPods Pro",
    "Samsung Galaxy Buds Pro", "Sony WF-1000XM4", "Bose SoundLink Revolve+", "Jabra Elite 85t", "Razer Kraken X",
    "HyperX Cloud II", "SteelSeries Arctis 7", "Logitech G Pro X", "Blue Yeti USB Microphone", "Rode NT-USB",
    "Elgato Stream Deck", "Acer Predator X27", "ASUS ROG Swift PG259QN", "LG 34GN850-B", "Samsung Odyssey G7",
    "Apple Watch Series 7", "Garmin Fenix 6", "Withings Steel HR", "Xiaomi Mi Band 6", "Huawei Watch GT 2 Pro",
    "Raspberry Pi 4 Model B", "Arduino Uno", "Intel NUC 11", "HP Omen 15", "Lenovo Legion 5 Pro",
    "Dell Alienware m15 R6", "Microsoft Xbox Series X", "Sony PlayStation 5", "Nintendo Switch OLED", "Valve Steam Deck"
]

# Function to generate a list of tech market items
def generate_tech_items(count):
    items = []
    used_names = set()  # To track used names
    for i in range(count):
        name = random.choice(product_names)
        barcode = f"{random.randint(100000000000, 999999999999)}"
        description = f"{name} - This is a high-quality {name.lower()}."
        
        if name not in used_names:
            used_names.add(name)
            item = Item (
                name =  name,
                barcode = barcode ,  # Random 12-digit barcode
                price = round(random.uniform(50, 1500), 2),  # Random price between 50 and 1500
                description = description
            )
            items.append(item)
            
    return items

# Function to generate a random username
def generate_username(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate a random email address
def generate_email(username):
    return f"{username}@example.com"

#  Function to create and add users to the database
def create_users(count):
    users = []
    for _ in range(count):
        username = generate_username()
        email = generate_email(username)
        password = "password123"  # Use a default password for simplicity
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            username=username,
            email_address=email,
            password_hash=password_hash,
            budget=1000  # Default budget
        )
        users.append(user)

    return users

def add_initial_users(app): 
     with app.app_context():
        # Drop all existing items
        try:
            db.session.query(User).delete()
            db.session.commit()
            print("All existing Users deleted!")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Users: {e}")
            return f"Users: {e}"
     # Check if items already exist to avoid duplicates
        if not User.query.first():
            users = create_users(10)
            
            try:
                db.session.add_all(users)
                db.session.commit()
                print("Users added successfully!")
                return "Users added successfully!"
            except Exception as e:
                db.session.rollback()
                print(f"Error adding Users: {e}")
                return f"Error: {e}"
        else:
            print("Users already exist in database")
            return "Users already exist in database"
        
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
            items = generate_tech_items(300)
            
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
