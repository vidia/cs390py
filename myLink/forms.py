from flask_wtf import Form
from wtforms import TextField, PasswordField
from  wtforms import validators
from wtforms.validators import DataRequired


class LoginForm(Form):
    """Form class for user login."""
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignupForm(Form):
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    # accept_tos = BooleanField('I accept the TOS', [validators.Required()])
