from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask.ext.login import login_required, current_user
from .models.user import User, Friend
from myLink import db

user_route = Blueprint('user_route', __name__,
                        template_folder='templates')

@user_route.route("/profile", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)

@user_route.route("/users", methods=["GET"])
@login_required
def users():
    users = User.query.all()
    # Add code to toggle if a person is the friend of the current_user
    return render_template("users.html", users=users)


@user_route.route('/user/<int:user_id>/friend/request')
def request_friend(user_id):
    friend = Friend(current_user.id, user_id)
    friend2 = Friend(user_id, current_user.id)
    db.session.add(friend)
    db.session.add(friend2)
    db.session.commit()
    flash("Friend request sent")
    return redirect(request.args.get('next') or \
           request.referrer or \
           url_for('index'))

@user_route.route('/user/<int:user_id>/friend/accept')
def accept_request(user_id):
    friend = Friend.query.filter(Friend.user_id==user_id)\
        .filter(Friend.friend_id==current_user.id).first()

    friend2 = Friend.query.filter(Friend.user_id==current_user.id)\
        .filter(Friend.friend_id==user_id).first()

    friend.confirm()
    friend2.confirm()
    db.session.commit()
    return redirect(request.args.get('next') or \
           request.referrer or \
           url_for('index'))

@user_route.route('/user/<int:user_id>/friend/reject')
def reject_request(user_id):
    friend = Friend.query.filter(Friend.user_id==user_id)\
        .filter(Friend.friend_id==current_user.id).first()
    friend2 = Friend.query.filter(Friend.user_id==current_user.id)\
        .filter(Friend.friend_id==user_id).first()
    db.session.delete(friend)
    db.session.delete(friend2)
    db.session.commit()
    return redirect(request.args.get('next') or \
           request.referrer or \
           url_for('index'))

@user_route.route('/user/<int:user_id>/friend/cancel')
def cancel_request(user_id):
    friend = Friend.query.filter(Friend.user_id==user_id)\
        .filter(Friend.friend_id==current_user.id).first()
    friend2 = Friend.query.filter(Friend.user_id==current_user.id)\
        .filter(Friend.friend_id==user_id).first()
    db.session.delete(friend)
    db.session.delete(friend2)
    db.session.commit()
    return redirect(request.args.get('next') or \
           request.referrer or \
           url_for('index'))

@user_route.route("/friends")
def my_friends():
    return render_template("friends.html", friends=current_user.friends)
