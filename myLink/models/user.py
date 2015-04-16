from myLink import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    """Copied from: https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/"""
    authenticated = db.Column(db.Boolean, default=False)

    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password


    def __repr__(self):
        return '<User %r>' % self.username

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
