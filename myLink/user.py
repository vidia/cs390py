from flask import render_template, redirect, url_for, flash, Blueprint, request, send_file
from flask.ext.login import login_required, current_user
from .models.user import User, Friend
from myLink import db
from urllib import parse
from .forms import UploadForm, UpdateProfileForm
import os
from werkzeug import secure_filename

from myLink import bcrypt


user_route = Blueprint('user_route', __name__,
                       template_folder='templates')


@user_route.route("/feed", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template("feed.html", user=user)


@user_route.route("/profile", methods=["GET"])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)


@user_route.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files[form.image.name]
        if file:
            print(form.image.data)
            filename = secure_filename(form.image.data.filename)

            raw_file = open(os.path.join("./files", filename), "wb+")
            file.save(raw_file)
            raw_file.close()

            flash("File Uploaded", "success")
            return redirect(url_for('user_route.profile'))
    return render_template("upload.html", form=form)


@user_route.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    print("In edit profile function")

    form = UpdateProfileForm(obj=current_user)

    print("Created form")

    if form.validate_on_submit():
        # save the provided values.
        print("Form was posted/valid")

        profilePhoto = request.files[form.image.name]
        if profilePhoto:

            filename = os.path.join(
                "./files", str(current_user.id), "_profile.jpg")

            print(filename)

            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

            if os.path.exists(filename):
                print("File exists, deleting it")
                os.remove(filename)

            raw_file = open(filename, "wb+")
            profilePhoto.save(raw_file)
            raw_file.close()

            current_user.image = filename

        if form.first_name.data:  # if they entered the name
            current_user.first_name = form.first_name.data
        if form.last_name.data:  # if they entered the name
            current_user.last_name = form.last_name.data
        if form.new_password.data or form.current_password.data\
                or form.confirm.data:
            if form.new_password.data and form.current_password.data\
                    and form.confirm.data:
                if form.confirm.data == form.new_password.data:
                    if bcrypt.check_password_hash(current_user.password, form.current_password.data):
                        pw_hash = bcrypt.generate_password_hash(
                            form.new_password.data)
                        flash("Password Updated Successfully", "success")
                    else:
                        flash("Current password not correct", "warning")
                else:
                    flash("Passwords do not match", "warning")
            else:
                flash(
                    "To change password you must fill out all password fields", "warning")

        flash("Profile updated successfully", "success")
        db.session.commit()

        return redirect(url_for('user_route.edit_profile'))
    else:
        print("Form not posted or not valid")
        if request.method == "POST":
            print("Not valid")
            return redirect(url_for('user_route.edit_profile'))

        return render_template("update-profile.html", form=form)


@user_route.route("/user/<int:user_id>/profile.jpg")
def getProfilePic(user_id):
    filename = os.path.join("../files", str(user_id), "_profile.jpg")
    if os.path.exists(filename):
        return send_file(filename, mimetype='image/jpeg')
    else:
        return send_file("../files/default/_profile.jpg")


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
    return redirect(request.args.get('next') or
                    request.referrer or
                    url_for('index'))


@user_route.route('/user/<int:user_id>/friend/accept')
def accept_request(user_id):
    friend = Friend.query.filter(Friend.user_id == user_id)\
        .filter(Friend.friend_id == current_user.id).first()

    friend2 = Friend.query.filter(Friend.user_id == current_user.id)\
        .filter(Friend.friend_id == user_id).first()

    friend.confirm()
    friend2.confirm()
    db.session.commit()
    return redirect(request.args.get('next') or
                    request.referrer or
                    url_for('index'))


@user_route.route('/user/<int:user_id>/friend/reject')
def reject_request(user_id):
    friend = Friend.query.filter(Friend.user_id == user_id)\
        .filter(Friend.friend_id == current_user.id).first()
    friend2 = Friend.query.filter(Friend.user_id == current_user.id)\
        .filter(Friend.friend_id == user_id).first()
    db.session.delete(friend)
    db.session.delete(friend2)
    db.session.commit()
    return redirect(request.args.get('next') or
                    request.referrer or
                    url_for('index'))


@user_route.route('/user/<int:user_id>/friend/cancel')
def cancel_request(user_id):
    friend = Friend.query.filter(Friend.user_id == user_id)\
        .filter(Friend.friend_id == current_user.id).first()
    friend2 = Friend.query.filter(Friend.user_id == current_user.id)\
        .filter(Friend.friend_id == user_id).first()
    db.session.delete(friend)
    db.session.delete(friend2)
    db.session.commit()
    return redirect(request.args.get('next') or
                    request.referrer or
                    url_for('index'))


@user_route.route("/user/verify/<token>")
def verify(token):
    normalized = parse.unquote_plus(token)
    user = User.query.filter(User.emailToken == token).first()
    if user:
        user.authenticated = True
        return redirect(url_for('profile'))


@user_route.route("/friends")
def my_friends():
    return render_template("friends.html", friends=current_user.friends)
