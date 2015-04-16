from flask import Flask
app = Flask(__name__)

from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)


from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'foo'
app.config['WTF_CSRF_KEY'] = 'foo'

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()
bcrypt.init_app(app)


import myLink.views
import myLink.login
