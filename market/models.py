from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("Item", backref="owned_user", lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # Generate a random salt using bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            plain_text_password.encode("utf-8"), salt
        ).decode("utf-8")

    def __repr__(self):
        return f"User {self.username}"


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=True)

    def __repr__(self):
        return f"Item {self.name}"
