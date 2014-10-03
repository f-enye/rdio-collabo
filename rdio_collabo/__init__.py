from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from OAuthClasses.RdioOAuth import RdioAuthenticator

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'Login'

rdioOAuth = RdioAuthenticator()

from rdio_collabo import views, models
