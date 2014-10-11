# flask related functions
from flask import render_template, url_for, redirect, g, request, jsonify, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from rdio_collabo import app, db, lm, rdioOAuth
from .forms import PlaylistForm
from .models import User, Playlist


# OAuth related functions.
from OAuthClasses.RdioOAuth import GetRequestTokenCredentials, CreateLoginString, CreateRequestToken, GetAccessTokenCredentials, RdioGetCurrentUser, RdioCreatePlaylist, RdioGetPlaylists


#################Template Rendering Functions##############
@app.route('/') 
@app.route('/index')
@login_required
def Index():
    playlists = RdioGetPlaylists(g.user.client_key, rdioOAuth.consumer)
    ownerPlaylists = [playlist['name'] for playlist in playlists['result']['owned']]
    return render_template('index.html', ownerPlaylists=ownerPlaylists)

@app.route('/playlists', methods=['GET'])
def  GetPlaylists():
    return jsonify(RdioGetPlaylists(g.user.client_key, rdioOAuth.consumer))

@app.route('/playlists/create', methods=['POST'])
def CreatePlaylist():
    form = PlaylistForm()

    if form.validate_on_submit():
        playlistInfo = {}
        playlistInfo['name'] = form.name.data
        playlistInfo['description'] = form.description.data
        return jsonify(RdioCreatePlaylist(g.user.user_name, g.user.password, rdioOAuth.consumer, playlistInfo))
    return jsonify({'fail': 'you lose!'})

@app.route('/playlists/nearby', methods=['POST'])
def NearbyPlaylist():
    playlists = Playlist.query.all()
    
    dictPlaylist = {'playlists': []}
    for playlist in playlists:
        dictPlaylist['playlists'].append(playlist.serialize())

    return jsonify(dictPlaylist)

@app.route('/add/<song_id>', methods=['POST'])
def add(song_id):
    return webservice.add(song_id)

@app.route('/search/<query>', methods=['POST'])
def search(query):
    return webservice.search(query)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('Index'))

    return render_template('login.html', title='Log In')

@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('Login'))

#############Helper Functions##############
@app.before_request
def BeforeRequest():
    g.user = current_user

#Used for flask-login
@lm.user_loader
def LoadUser(user_id):
    return User.query.get(int(user_id))

#############OAuth Functions###############

@app.route('/rdio/login')
def RdioOAuthLogin():
    requestTokenCredentials = GetRequestTokenCredentials('http://localhost:5000' + url_for('RdioLoginCallback'), rdioOAuth.client)
    session["oauth_token_secret"] = requestTokenCredentials["oauth_token_secret"]
    return redirect(CreateLoginString(requestTokenCredentials["login_url"], requestTokenCredentials["oauth_token"]))

@app.route('/rdio/login/callback')
def RdioLoginCallback():
    requestToken = CreateRequestToken(request.args["oauth_token"], session["oauth_token_secret"])
    requestToken.set_verifier(request.args["oauth_verifier"])
    
    accessTokenCredentials = GetAccessTokenCredentials(rdioOAuth.consumer, requestToken)
    rdioCurrentUser = RdioGetCurrentUser(accessTokenCredentials["oauth_token"], 
                                         accessTokenCredentials["oauth_token_secret"], 
                                         rdioOAuth.consumer)

    #See if user currently exists.
    #If the user does not exist create it.
    #Otherwise update the access token.
    user = User.query.filter_by(client_key=rdioCurrentUser["result"]["key"]).first()
    if user is None:
        user = User(client_key=rdioCurrentUser["result"]["key"], 
                    user_name=accessTokenCredentials["oauth_token"], 
                    password=accessTokenCredentials["oauth_token_secret"])
        db.session.add(user)
    else:      
        user.user_name = accessTokenCredentials["oauth_token"]
        user.password = accessTokenCredentials["oauth_token_secret"]
    
    db.session.commit()
    login_user(user) 

    return redirect(url_for("Index"))
