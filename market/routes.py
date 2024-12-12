from flask import Blueprint
from flask import render_template
from market.models import Item

# Create a Blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')

@main.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)
