from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from market.models import db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm


# Create a Blueprint for routes
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home_page():
    return render_template("home.html")


@main.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@main.route("/registration", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():

        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("main.market_page"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"{err_msg[0]}", category="danger")

    return render_template("registration.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f"logged in", category="success")
        

    return render_template("login.html", form=form)
