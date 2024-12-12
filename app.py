from flask import render_template
from .init_data import add_initial_items
from .__init__ import create_app
from .item import db, Item


app = create_app()

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route('/init-db')
def init_db():
   return add_initial_items(app)