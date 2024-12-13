from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists!")

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email already exists!")

    username = StringField(
        label="username", validators=[Length(min=2, max=30), DataRequired()]
    )
    email_address = EmailField(label="email", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="password", validators=[Length(min=6), DataRequired()]
    )
    confirm_password = PasswordField(
        label="confirm password", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField(label="submit")


class LoginForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user is None:
            raise ValidationError("Username not found!")

    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired()])

    submit = SubmitField(label="submit")


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item!")
