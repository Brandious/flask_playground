from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from market.models import db
from market.models import Item, User
from market.forms import PurchaseItemForm, RegisterForm, LoginForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

# Create a Blueprint for routes
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home_page():
    return render_template("home.html")


@main.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                    category="success",
                )
            else:
                flash(
                    f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                    category="danger",
                )
        # Sell Item Logic
        sold_item = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f"Congratulations! You sold {s_item_object.name} back to market!",
                    category="success",
                )
            else:
                flash(
                    f"Something went wrong with selling {s_item_object.name}",
                    category="danger",
                )
        return redirect(url_for("main.market_page"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template(
            "market.html",
            items=items,
            purchase_form=purchase_form,
            owned_items=owned_items,
            selling_form=selling_form,
        )


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
        flash(f"user created", category="success")
        login_user(user_to_create)
        return redirect(url_for("main.market_page"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"{err_msg[0]}", category="danger")

    return render_template("registration.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f"logged in", category="success")
            return redirect(url_for("main.market_page"))
        else:
            flash(f"Something went wrong", category="warning")

    return render_template("login.html", form=form)


@main.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash(f"User succesfully logged out", category="info")
    return redirect(url_for("main.home_page"))
