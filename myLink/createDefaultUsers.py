from .models.user import User, Friend
from myLink import bcrypt, db
from flask.ext.login import login_user


user1 = User.query.filter_by(email="dmtschida1@gmail.com").first()
user2 = User.query.filter_by(email="dmtschida2@gmail.com").first()
if not user1 and not user2:
    pw_hash = bcrypt.generate_password_hash("foo")
    usera = User("dmtschida1@gmail.com",
                pw_hash)
    usera.first_name = "David"
    usera.last_name = "Tschida"
    usera.authenticated = True
    # login_user(usera, remember=True)
    db.session.add(usera)
    db.session.commit()

    pw_hash = bcrypt.generate_password_hash("foo")
    userb = User("dmtschida2@gmail.com",
                pw_hash)
    userb.first_name = "Charles"
    userb.last_name = "Norris"
    db.session.add(userb)
    db.session.commit()


    pw_hash = bcrypt.generate_password_hash("foo")
    userc = User("dtschida@purdue.edu",
                pw_hash)
    userc.first_name = "User"
    userc.last_name = "Person"
    db.session.add(userc)
    db.session.commit()


    friend = Friend(usera.id, userb.id, usera.id)
    friend2 = Friend(userb.id, usera.id, usera.id)
    friend.confirm()
    friend2.confirm()
    db.session.add(friend)
    db.session.add(friend2)
    db.session.commit()


    friend = Friend(usera.id, userc.id, usera.id)
    friend2 = Friend(userc.id, usera.id, usera.id)
    friend.confirm()
    friend2.confirm()
    db.session.add(friend)
    db.session.add(friend2)
    db.session.commit()
