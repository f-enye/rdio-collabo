from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from OAuthClasses.RdioOAuth import RdioAuthenticator
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'Login'

csrf = CsrfProtect()
csrf.init_app(app)

rdioOAuth = RdioAuthenticator()

from rdio_collabo import views, models
