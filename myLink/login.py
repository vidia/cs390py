from myLink import login_manager, bcrypt, db
from myLink.models.user import User

from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required, login_user, logout_user, current_user

from .forms import LoginForm, SignupForm

from .mail import sendVerificationEmail

login_route = Blueprint('login', __name__,
                        template_folder='templates')

@login_route.route("/cookies", methods=["GET", "POST"])
def cookies():
    return str(request.cookies)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@login_route.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("An account already exists for this email")
            return render_template('signup.html', form=form)

        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(form.email.data,
                    pw_hash)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering, an email has been sent to verify your account', "info")

        sendVerificationEmail(user)

        return redirect(url_for('user_route.profile'))
    return render_template('signup.html', form=form)

@login_route.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flash("The user was logged in", "info")
                return redirect(url_for("user_route.profile"))
    return render_template("login.html", form=form)

@login_route.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")
