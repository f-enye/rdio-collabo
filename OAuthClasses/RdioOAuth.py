"""
webservice

This module is an interface to an external music API.
"""

import oauth2 as oauth
import urllib
import urlparse
import json

RdioCollaborationModes = {
    'NoCollaboration': 0,
    'CollaborateAllUsers': 1,
    'CollaborateFollowedUsers': 2
    }

RDIO_REQUEST_TOKEN_URL = 'http://api.rdio.com/oauth/request_token'
RDIO_ACCESS_TOKEN_URL = 'http://api.rdio.com/oauth/access_token'
RDIO_API_URL = 'http://api.rdio.com/1/'

# Request Token Functions

def GetRequestTokenCredentials(callback, client):
    response, content = client.request(RDIO_REQUEST_TOKEN_URL, 'POST', urllib.urlencode({'oauth_callback':callback}))
    return dict(urlparse.parse_qsl(content)) 

def CreateLoginString(loginURL, oauthToken):
    return loginURL + "?oauth_token=" + oauthToken

def CreateRequestToken(oauthToken, oauthTokenSecret):
    return oauth.Token(oauthToken, oauthTokenSecret)

def GetAccessTokenCredentials(consumer, requestToken):
    # upgrade the request token to an access token
    client = oauth.Client(consumer, requestToken)
    response, content = client.request(RDIO_ACCESS_TOKEN_URL, 'POST')
    # return access token credentials
    return dict(urlparse.parse_qsl(content))

#Access Token Functions

def RdioGetCurrentUser(oauthToken, oauthTokenSecret, consumer):
    # Get current user information.
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)
    response, content = client.request(RDIO_API_URL, 'POST', urllib.urlencode({'method': 'currentUser'}))
    return json.loads(content)

def RdioCreatePlaylist(oauthToken, oauthTokenSecret, consumer, playlistInfo):
    #Create a playlist
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)
    
    # We require the playlist name, description, and tracks.
    # The tracks field can have string with white space to indicate we don't want to
    # include tracks yet.
    # We set the collaboration Mode of the playlist to collaborate with all users.
    response, content = client.request(RDIO_API_URL, 'POST', 
                                       urllib.urlencode({'method': 'createPlaylist', 
                                                         'name': playlistInfo['name'], 
                                                         'description': playlistInfo['description'], 
                                                         'tracks': " ", 
                                                         'collaborationMode': RdioCollaborationModes['CollaborateAllUsers']}))
    return json.loads(content)

def RdioGetPlaylists(userKey, oauthToken, oauthTokenSecret, consumer):
    #Get playlists
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)

    response, content = client.request(RDIO_API_URL, 'POST', 
                                       urllib.urlencode({'method': 'getPlaylists', 'user': userKey}))
    return json.loads(content)

def RdioSearchTracks(query, oauthToken, oauthTokenSecret, consumer):
    #Search for artist, album, track
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)

    response, content = client.request(RDIO_API_URL, 'POST',
                                       urllib.urlencode({'method': 'search', 'query': query, 'types': 'Track'}))
    return json.loads(content)

def RdioSearchPlaylists(query, oauthToken, oauthTokenSecret, consumer):
    #Search for playlists
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)

    response, content = client.request(RDIO_API_URL, 'POST',
                                       urllib.urlencode({'method': 'search', 'query': query, 'types': 'Playlist'}))
    return json.loads(content)

def RdioIsTrackKeyValid(trackKey, oauthToken, oauthTokenSecret, consumer):
    # returns true or false based on whether the track key is valid or not.
    trackKeyValid = False

    accessToken = oauth.Token(oauthToken, oauthTokenSecret)
    client = oauth.Client(consumer, accessToken)
    response, content = client.request(RDIO_API_URL, 'POST', 
                                       urllib.urlencode({'method': 'get', 'keys': trackKey}))
    result = json.loads(content)

    # check if status is ok.
    if u'ok' == result['status']:
        trackKeyValid = RdioResultValid(result['result'])

    return trackKeyValid

def RdioGetTrackInfo(trackKey, oauthToken, oauthTokenSecret, consumer):
    #returns track info based on the given track key.
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)
    client = oauth.Client(consumer, accessToken)
    response, content = client.request(RDIO_API_URL, 'POST',
                                       urllib.urlencode({'method': 'get', 'keys': trackKey}))

    result = json.loads(content)
    # check if status is ok
    if u'ok' == result['status'] and RdioResultValid(result['result']):
        return result
    return {'status': 'error', 'message': 'Bad status, or invalid result.'}

def RdioResultValid(result):
    # the result returned should have valid tracks only, if the track is invalid, the dictionary should be empty.
    return len(result) == 1
def RdioAddTrackToPlaylist(playlistKey, trackKey, oauthToken, oauthTokenSecret, consumer):
    # add track to playlist
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)
    client = oauth.Client(consumer, accessToken)
    response, content = client.request(RDIO_API_URL, 'POST',
                                       urllib.urlencode({'method': 'addToPlaylist', 
                                                         'playlist': playlistKey, 
                                                         'tracks': trackKey}))
    return json.loads(content)

class RdioAuthenticator(object):
    """docstring for RdioAuthenticator"""
    
    consumer = None
    client = None

    def BuildConsumerAndClient(self, consumerKey, consumerSecret):
        # create the OAuth consumer credentials.
        self.consumer = oauth.Consumer(consumerKey, consumerSecret)

        # build client basked on consumer credentials. 
        self.client = oauth.Client(self.consumer)
