from myLink import login_manager, bcrypt, db
from myLink.models.user import User, Circle, CircleMember, CircleOwnership

from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required, current_user

from .forms import LoginForm, SignupForm, CreateCircleForm

from .mail import sendVerificationEmail
from flask_wtf import Form
from wtforms import SelectField
from  wtforms import validators, widgets
from wtforms.validators import DataRequired



circles_route = Blueprint('circles', __name__,
                        template_folder='templates')


@circles_route.route("/circles", methods=["GET", "POST"])
@login_required
def circles():

    return render_template("circles.html", user=current_user)



@circles_route.route("/circles/create", methods=["GET", "POST"])
@login_required
def createcircles():
    form = CreateCircleForm()

    if form.validate_on_submit():


        newcircle = Circle(current_user.id, form.name.data)
        db.session.add(newcircle)
        db.session.commit()
        db.session.add(CircleOwnership(current_user.id, newcircle.id))
        db.session.commit()

        return redirect(url_for('circles.circles'))

    return render_template("create-circle.html", user=current_user, form=form)

@circles_route.route("/circles/<int:circle_id>/delete", methods=["GET", "POST"])
@login_required
def delete(circle_id):

    co = CircleOwnership.query.filter(CircleOwnership.circle_id == circle_id).first()
    db.session.delete(co)

    c = Circle.query.filter(Circle.id == circle_id).first()
    db.session.delete(co)

    cml = CircleMember.query.filter(CircleMember.circle_id == circle_id)
    for cm in cml:
        db.session.delete(cm)

    db.session.commit()

    return redirect(url_for('circles.circles'))

@circles_route.route("/circles/<int:circle_id>/remove/<int:user_id>", methods=["GET", "POST"])
@login_required
def removeUser(circle_id, user_id):
    co = CircleOwnership.query.filter(CircleOwnership.circle_id == circle_id).first()
    c = Circle.query.filter(Circle.id == circle_id).first()
    cm = CircleMember.query.filter(CircleMember.circle_id == circle_id)\
        .filter(CircleMember.user_id == user_id).first()
    db.session.delete(cm)
    db.session.commit()

    return redirect(url_for('circles.circles'))


@circles_route.route("/circles/<int:circle_id>/add", methods=["GET"])
@login_required
def editCircle(circle_id):
    circle = Circle.query.filter(Circle.id == circle_id).first()
    return render_template("addtocircles.html", user=current_user, circle=circle)

@circles_route.route("/circles/<int:circle_id>/add/<int:user_id>", methods=["GET"])
@login_required
def addUserToCircle(circle_id, user_id):
    cm = CircleMember.query.filter(CircleMember.user_id == user_id).filter(CircleMember.circle_id == circle_id).first()
    if cm:
        flash("That person is already in the circle", "warning")
    else:
        db.session.add( CircleMember(user_id, circle_id) )
        db.session.commit()

    return redirect(url_for('circles.circles'))





@circles_route.route("/circles/test", methods=["GET", "POST"])
@login_required
def testCircles():

    newcircle = Circle(current_user.id, "My First Circle" )
    db.session.add(newcircle)
    db.session.commit()

    newcircle = Circle.query.filter(Circle.name == "My First Circle").first()

    print(str(newcircle.id))

    db.session.add(CircleOwnership(current_user.id, newcircle.id))
    db.session.commit()

    print(str(current_user.circles))

    otherperson = User.query.filter(User.id != current_user.id).first()
    print("Other user " + str(otherperson.id))

    db.session.add( CircleMember(otherperson.id, newcircle.id) )
    db.session.commit()

    print(newcircle.members)

    return str(current_user)
