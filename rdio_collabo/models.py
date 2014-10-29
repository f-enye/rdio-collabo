from rdio_collabo import db

#PlaylistTrack Table
Tracks = db.Table('Tracks', 
                  db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                  db.Column('track_id', db.Integer, db.ForeignKey('track.id'))
                 )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True)
    client_key = db.Column(db.String(120), index=True)

    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')

    # login manager required functions
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.user_name)

    def serialize(self):
        return {"user_name": self.user_name}

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.String(120), index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    tracks = db.relationship('Track', secondary=Tracks, backref=db.backref('playlists', lazy='dynamic'), lazy='dynamic')

    def serialize(self):
        return {'id': self.id, 'name': self.name}

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    artist = db.Column(db.String(120), index=True)
    rdioID = db.Column(db.String(120), index=True)
