# flask related functions
from flask import render_template, url_for, redirect, g, request, jsonify, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.socketio import emit, join_room, leave_room
from rdio_collabo import app, db, lm, rdioOAuthManager, socketio
from .forms import PlaylistForm, PlaylistSearchForm, AlbumsArtistsTracksSearchForm, AddTrackToPlaylistForm
from .models import User as UserModel
from .models import Playlist as PlaylistModel
from .models import Track as TrackModel

# OAuth related functions.
from OAuthClasses.RdioOAuth import (GetRequestTokenCredentials, CreateLoginString, 
                                    CreateRequestToken, GetAccessTokenCredentials, 
                                    RdioGetCurrentUser, 
                                    RdioSearchTracks,
                                    RdioSearchPlaylists,
                                    RdioGetTrackInfo)

#################Template Rendering Functions##############
@app.route('/') 
@app.route('/index')
@login_required
def Index():
    playlists = PlaylistModel.query.filter_by(user_id=g.user.id)
    ownerPlaylists = [{'id': playlist.id, 'name': playlist.name}
                      for playlist in playlists]
    return render_template('index.html', ownerPlaylists=ownerPlaylists)

@app.route('/playlists/<id>', methods=['GET'])
@login_required
def Playlist(id):
    playlist = PlaylistModel.query.filter_by(id=id).first()
    return render_template('playlist.html', playlist=playlist)

@app.route('/voting', methods=['GET'])
@login_required
def Voting():
    return render_template('voting.html')

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('Index'))

    return render_template('login.html', title='Log In')

@app.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Login'))

######################Socket.IO Calls############################
@socketio.on('connect', namespace='/playlist')
@login_required
def PlaylistConnect():
    emit('playlist connect response', {'status': u'ok', 'message': u'connected'})

@socketio.on('join', namespace='/playlist')
def OnJoin(data):
    BeforeRequest()
    join_room(data["room"])

    message = g.user.user_name + " has entered room " + data["room"]

    print message

    emit('room join response', {'status': u'ok', 'message': message}, room=data["room"])

@socketio.on('leave', namespace='/playlist')
def OnLeave(data):
    BeforeRequest()
    leave_room(data["room"])

    emit('room left response', {'status': u'ok', 'message': g.user.user_name + " has left room " + data["room"]}, room=data["room"])

@socketio.on('add track to playlist', namespace='/playlist')
@login_required
def AddTrackToPlaylist(message):
    BeforeRequest()
    response = {'status': u'error'}
    form = AddTrackToPlaylistForm(playlist_id=message['playlist_id'], track_rdioID=message['track_rdioID'], csrf_token=message['csrf_token'])

    if form.validate():
        playlistKey = form.playlist_id.data
        trackKey = form.track_rdioID.data

        playlist = PlaylistModel.query.filter_by(id=playlistKey).first()
        if playlist is not None:
            trackInfo = RdioGetTrackInfo(trackKey, g.user.user_name, g.user.password, rdioOAuthManager.consumer)['result']
            trackArtist = trackInfo[trackKey]['artist']
            trackName = trackInfo[trackKey]['name']

            track = TrackModel.query.filter_by(rdioID=trackKey).first()
            if track is None:
                track = TrackModel(artist=trackArtist, name=trackName, rdioID=trackKey)

            playlist.tracks.append(track)
            db.session.commit()
            response = {'status': u'ok', 'result': {'name': trackName, 'artist': trackArtist}}
    emit('add track to playlist response', response, room=playlistKey)

###################JSON Returning Calls##########################
@app.route('/playlists/create', methods=['POST'])
@login_required
def CreatePlaylist():
    form = PlaylistForm()

    if form.validate_on_submit():
        playlistInfo = {}
        playlistInfo['name'] = form.name.data
        playlistInfo['description'] = form.description.data
        
        playlist = PlaylistModel(name=playlistInfo['name'], description=playlistInfo['description'], user_id=g.user.id)
        db.session.add(playlist)
        db.session.commit()
        return jsonify({'status': u'ok', 'result': playlist.serialize()})
    return jsonify({'status': u'error', 'message': 'Invalid form data.'})

@app.route('/search/tracks', methods=['POST'])
@login_required
def SearchTracks():
    form = AlbumsArtistsTracksSearchForm()

    if form.validate_on_submit():
        query = form.query.data
        return jsonify(RdioSearchTracks(query, g.user.user_name, g.user.password, rdioOAuthManager.consumer))

@app.route('/playlists/nearby', methods=['POST'])
@login_required
def NearbyPlaylist():
    playlists = PlaylistModel.query.all()
    
    dictPlaylist = {'playlists': []}
    for playlist in playlists:
        dictPlaylist['playlists'].append(playlist.serialize())

    return jsonify(dictPlaylist)

@app.route('/search/playlists', methods=['POST'])
@login_required
def SearchPlaylists():
    form = PlaylistSearchForm()

    if form.validate_on_submit():
        query = form.query.data
        return jsonify(RdioSearchPlaylists(query, g.user.user_name, g.user.password, rdioOAuthManager.consumer))

#############Helper Functions##############
@app.before_request
def BeforeRequest():
    g.user = current_user

#Used for flask-login
@lm.user_loader
def LoadUser(user_id):
    return UserModel.query.get(int(user_id))

#############OAuth Functions###############

@app.route('/rdio/login')
def RdioOAuthLogin():
    requestTokenCredentials = GetRequestTokenCredentials('http://' + request.headers['Host'] + url_for('RdioLoginCallback'), rdioOAuthManager.client)
    session["oauth_token_secret"] = requestTokenCredentials["oauth_token_secret"]
    return redirect(CreateLoginString(requestTokenCredentials["login_url"], requestTokenCredentials["oauth_token"]))

@app.route('/rdio/login/callback')
def RdioLoginCallback():
    requestToken = CreateRequestToken(request.args["oauth_token"], session["oauth_token_secret"])
    requestToken.set_verifier(request.args["oauth_verifier"])
    
    accessTokenCredentials = GetAccessTokenCredentials(rdioOAuthManager.consumer, requestToken)
    rdioCurrentUser = RdioGetCurrentUser(accessTokenCredentials["oauth_token"], 
                                         accessTokenCredentials["oauth_token_secret"], 
                                         rdioOAuthManager.consumer)

    #See if user currently exists.
    #If the user does not exist create it.
    #Otherwise update the access token.
    user = UserModel.query.filter_by(client_key=rdioCurrentUser["result"]["key"]).first()
    if user is None:
        user = UserModel(client_key=rdioCurrentUser["result"]["key"], 
                         user_name=accessTokenCredentials["oauth_token"], 
                         password=accessTokenCredentials["oauth_token_secret"])
        db.session.add(user)
    else:      
        user.user_name = accessTokenCredentials["oauth_token"]
        user.password = accessTokenCredentials["oauth_token_secret"]
    
    db.session.commit()
    login_user(user) 

    return redirect(url_for("Index"))
