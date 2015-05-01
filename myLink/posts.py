from flask import render_template, redirect, url_for, flash, Blueprint, request, send_file, Response
from flask.ext.login import login_required, current_user
from .models.user import User, Friend, Post, Circle, PostCircles
from myLink import db
from urllib import parse
from .forms import UploadForm, UpdateProfileForm, PostForm
import os
from werkzeug import secure_filename

from myLink import bcrypt


post_route = Blueprint('post_route', __name__,
                       template_folder='templates')


@post_route.route("/post/<int:post_id>/image.jpg", methods=["GET"])
@login_required
def postimage(post_id):

    post = Post.query.filter(Post.id == post_id).first()

    if post:
        for circle in post.user.circles:
            circle = circle.circle

            print(circle.id)

            for member in circle.members:
                member = member.user

                print("Member", member.id)

                if current_user.id == member.id:
                    # I am in this user's circle.

                    filename = os.path.join(
                        "../files", str(post.user.id), str(post.id) ,"_image.jpg")

                    return send_file(filename, mimetype='image/jpeg')

        if post.user.id == current_user.id:
            print("My post")


            filename = os.path.join(
                "../files", str(post.user.id), str(post.id) ,"_image.jpg")

            print(filename)
            return send_file(filename, mimetype='image/jpeg')


    return Response("You don't have permission to see that", 401, {'WWWAuthenticate':'Basic realm="No permission to view"'})



@post_route.route("/feed", methods=["GET"])
@login_required
def feed():
    user = current_user

    posts = []

    for friend in current_user.friends:
        friend = friend.other(current_user.id)

        for circle in friend.circles:
            circle = circle.circle

            for member in circle.members:
                member = member.user

                if current_user.id == member.id:
                    # I am in this friend's circle.

                    pc = PostCircles.query.filter(PostCircles.circle_id == circle.id)

                    for post in pc:
                        post = post.post

                        posts.append(post)

    myposts = Post.query.filter(Post.user_id == current_user.id)

    for post in myposts:
        posts.append(post)


    uposts = set()
    uposts_add = uposts.add
    posts_unique = [ x for x in posts if not (x in uposts or uposts_add(x))]


    return render_template("feed.html", posts=posts_unique, user=user, title="My Feed", form = PostForm())


@post_route.route('/post', methods=['POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'POST':

        if form.content.data:
            post = Post()

            post.content = form.content.data
            post.user_id = current_user.id

            db.session.add(post)
            db.session.commit()

            file = request.files[form.image.name]
            if file:
                print(form.image.data)
                filename = os.path.join(
                    "./files", str(current_user.id), str(post.id) ,"_image.jpg")

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                if os.path.exists(filename):
                    print("File exists, deleting it")
                    os.remove(filename)

                post.image = filename

                raw_file = open(filename, "wb+")
                file.save(raw_file)
                raw_file.close()

                flash("File Uploaded", "success")


            if request.form.getlist('demoSel[]'):

                circles = request.form.getlist('demoSel[]')

                for circle in circles:
                    db.session.add(PostCircles(post.id, circle))

            db.session.add(post)
            db.session.commit()

        return redirect(url_for('post_route.feed'))

@post_route.route("/foo/edit", methods=['GET', 'POST'])
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

        return render_template("update-profile.html", form=form, user=current_user, title="Edit Profile")
