from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import Required, Email, EqualTo

class LoginForm(Form):
    user_name = TextField('user_name', validators=[Required(), Email(message=u'Invalid email address')])
    #Not an encrypted PasswordField
    password = PasswordField('password', validators=[Required()])

class SignupForm(Form):
    user_name = TextField('user_name', validators=[Required(), Email(message=u'Invalid email address')])
    password = PasswordField('password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('confirm_password', validators=[Required()])

class PlaylistForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextField('description')

class PlaylistSearchForm(Form):
    query = TextField('query', validators=[Required()])

class AlbumsArtistsTracksSearchForm(Form):
    query = TextField('query', validators=[Required()])

class AddTrackToPlaylistForm(Form):
    playlist_id = IntegerField('playlist_key', validators=[Required()])
    track_rdioID = TextField('track_key', validators=[Required()])
