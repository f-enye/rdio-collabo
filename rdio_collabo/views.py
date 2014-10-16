# flask related functions
from flask import render_template, url_for, redirect, g, request, jsonify, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from rdio_collabo import app, db, lm, rdioOAuthManager
from .forms import PlaylistForm
from .models import User as UserModel
from .models import Playlist as PlaylistModel

# OAuth related functions.
from OAuthClasses.RdioOAuth import GetRequestTokenCredentials, CreateLoginString, CreateRequestToken, GetAccessTokenCredentials, RdioGetCurrentUser, RdioCreatePlaylist, RdioGetPlaylists, RdioSearch

#################Template Rendering Functions##############
@app.route('/') 
@app.route('/index')
@login_required
def Index():
    playlists = RdioGetPlaylists(g.user.client_key, g.user.user_name, g.user.password, rdioOAuthManager.consumer)
    ownerPlaylists = [{'key': playlist['key'], 'name': playlist['name']} 
                      for playlist in playlists['result']['owned']]
    return render_template('index.html', ownerPlaylists=ownerPlaylists)

@app.route('/playlists/<key>', methods=['GET'])
def Playlist(key):
    playlists = RdioGetPlaylists(g.user.client_key, g.user.user_name, g.user.password, rdioOAuthManager.consumer)
    # Since playlist keys should be unique, we should only be retrieving one playlist. It should be the,
    # first and last one in the list.
    selectPlaylist = [playlist for playlist in playlists['result']['owned'] if playlist['key'] == key][0]
    return render_template('playlist.html', playlist=selectPlaylist)

@app.route('/voting', methods=['GET'])
def Voting():
    return 'yo'

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('Index'))

    return render_template('login.html', title='Log In')

@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('Login'))

###################Rdio API CALLS##########################

@app.route('/playlists/create', methods=['POST'])
def CreatePlaylist():
    form = PlaylistForm()

    if form.validate_on_submit():
        playlistInfo = {}
        playlistInfo['name'] = form.name.data
        playlistInfo['description'] = form.description.data
        return jsonify(RdioCreatePlaylist(g.user.user_name, g.user.password, rdioOAuthManager.consumer, playlistInfo))
    return jsonify({'fail': 'you lose!'})

@app.route('/search/<query>', methods=['POST'])
def Search(query):
    print query
    return jsonify(RdioSearch(query, g.user.user_name, g.user.password, rdioOAuthManager.consumer))

@app.route('/playlists/nearby', methods=['POST'])
def NearbyPlaylist():
    playlists = PlaylistModel.query.all()
    
    dictPlaylist = {'playlists': []}
    for playlist in playlists:
        dictPlaylist['playlists'].append(playlist.serialize())

    return jsonify(dictPlaylist)

@app.route('/add/<song_id>', methods=['POST'])
def add(song_id):
    return webservice.add(song_id)

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
    requestTokenCredentials = GetRequestTokenCredentials('http://localhost:5000' + url_for('RdioLoginCallback'), rdioOAuthManager.client)
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
