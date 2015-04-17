from myLink import app, login_manager, bcrypt, db
from myLink.models.user import User

from flask import render_template, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required, login_user, logout_user, current_user

from .forms import LoginForm

# login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)


@app.route("/login", methods=["GET", "POST"])
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
                flash("The user was logged in")
                return redirect("/profile")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")
