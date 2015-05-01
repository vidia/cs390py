from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
app.config['SECRET_KEY'] = 'foo'
app.config['WTF_CSRF_KEY'] = 'foo'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.setup_app(app)
login_manager.login_view = "/login"

db = SQLAlchemy(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

from myLink.login import login_route
app.register_blueprint(login_route)

from myLink.user import user_route
app.register_blueprint(user_route)

from myLink.circles import circles_route
app.register_blueprint(circles_route)

from myLink.posts import post_route
app.register_blueprint(post_route)


# import myLink.createDefaultUsers
