from flask import render_template, url_for, redirect, g, request, flash, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from rdio_collabo import app, db, lm, rdioOAuth
from forms import LoginForm, SignupForm
from models import User, Playlist
from OAuthClasses.RdioOAuth import RdioRequestTokenHandler, RdioAccessTokenHandler
import threading, webbrowser

#rdio-collabo ported modules
import webservice # An interface to an external music API.


#################Template Rendering Functions##############
@app.route('/') 
@app.route('/index')
# @login_required
def Index():
    requestTokenHandler = RdioRequestTokenHandler()
    requestTokenHandler.SetClientAndConsumer(rdioOAuth.client, rdioOAuth.consumer)
    threading.Timer(1.25, lambda: webbrowser.open(requestTokenHandler.GetLoginString('127.0.0.1:5000' + url_for('RdioLoginCallback')))).start()
    # return render_template("index.html")

@app.route('/rdio/login/callback')
def RdioLoginCallback():
    oauthToken = request.args.get('oauth_token')
    oauthVerifer = request.args.get('oauth_verifier')

    print oauthToken
    print oauthVerifer

    rdioOAuth.OAuthVerfier(oauthToken, oauthVerifer)
    rdioOAuth.UpgradeRequestTokenToAccessToken()
    # return redirect('Hello')

@app.route('/hello')
def Hello():
    return "hello"

@app.route('/playlists/new/<name>', methods=['POST'])
def NewPlaylist(name):
    webservice.newPlaylist(name)
    playlist = Playlist(name=name)
    db.session.add(playlist)
    db.session.commit()
    return render_template('playlist.html', name=name)

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

    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        user = User.query.filter_by(user_name = user_name).first()
        if user is not None and password == user.password:
            login_user(user)
            return redirect(request.args.get("next", url_for("Index")))
        else:
            flash("Invalid username or password")

    return render_template('login.html', title='Log In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('Index'))

    form = SignupForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        user = User(user_name=user_name, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('Login'))

    return render_template('signup.html', title='Sign Up', form=form)

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
