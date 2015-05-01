from myLink import db
import bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))

    image = db.Column(db.String(120))

    emailToken = db.Column(db.String(120), unique=True)

    """Copied from: https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/"""
    authenticated = db.Column(db.Boolean, default=False)
    password = db.Column(db.String)

    circles = db.relationship('CircleOwnership', backref='CircleOwnership.owner_id',\
        primaryjoin='User.id==CircleOwnership.owner_id', lazy='joined')

    friends = db.relationship('Friend', backref='Friend.friend_id',\
        primaryjoin='User.id==Friend.user_id', lazy='joined')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.emailToken = bcrypt.gensalt()

    def __repr__(self):
        return '<User %r>' % self.email

    """Copied from: https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/"""
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements. EDIT: Changed to ID as primary key"""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False




class Friend(db.Model):
    __tablename__ = 'friend'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    initiator_id = db.Column(db.Integer, db.ForeignKey(User.id))

    request_status = db.Column(db.Boolean)

    user = db.relationship('User', foreign_keys='Friend.user_id')
    friend = db.relationship('User', foreign_keys='Friend.friend_id')
    initiator = db.relationship('User', foreign_keys='Friend.initiator_id')

    def __init__(self, user, friend, initiator):
        self.user_id = user
        self.friend_id = friend
        self.initiator_id = initiator
        self.request_status = False

    def confirm(self):
        self.request_status = True

    def mine(self, id):
        if self.user_id == id:
            return self.user_id
        elif self.friend_id == id:
            return self.friend_id
        else:
            return None

    def other(self, id):
        if self.user_id == id:
            return self.friend
        elif self.friend_id == id:
            return self.user
        else:
            return None


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship('User', foreign_keys='Post.user_id')

    content = db.Column(db.String(2000))
    image = db.Column(db.String(120))


    circles_list = db.relationship('PostCircles', backref='PostCircles.post_id',\
        primaryjoin='Post.id==PostCircles.post_id', lazy='joined')


class Circle(db.Model):
    __tablename__ = 'circle'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120))

    members = db.relationship('CircleMember', backref='CircleMember.circle_id',\
        primaryjoin='Circle.id==CircleMember.circle_id', lazy='joined')

    def __init__(self, owner_id, name):
        self.name = name
        self.owner_id = owner_id


class PostCircles(db.Model):
    __tablename__ = 'PostCircles'

    post_id = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey(Circle.id), primary_key=True)

    post = db.relationship('Post', foreign_keys='PostCircles.post_id')
    circle = db.relationship('Circle', foreign_keys='PostCircles.circle_id')

    def __init__(self, post_id, circle_id):
        self.post_id = post_id
        self.circle_id = circle_id

class CircleMember(db.Model):
    __tablename__ = "CircleMember"

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey(Circle.id), primary_key=True)

    user = db.relationship('User', foreign_keys='CircleMember.user_id')
    circle = db.relationship('Circle', foreign_keys='CircleMember.circle_id')

    def __init__(self, user_id, circle_id):
        self.user_id = user_id
        self.circle_id = circle_id

class CircleOwnership(db.Model):
    __tablename__ = 'circleownership'

    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey(Circle.id), primary_key=True)

    owner = db.relationship('User', foreign_keys='CircleOwnership.owner_id')
    circle = db.relationship('Circle', foreign_keys='CircleOwnership.circle_id')

    def __init__(self, owner_id, circle_id):
        self.owner_id = owner_id
        self.circle_id = circle_id

db.create_all()
