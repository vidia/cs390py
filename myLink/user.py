from flask import render_template, redirect, url_for, flash, Blueprint
from flask.ext.login import login_required, current_user

user_route = Blueprint('user_route', __name__,
                        template_folder='templates')

@user_route.route("/profile", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)
