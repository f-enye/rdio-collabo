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

# Request Token Functions

def GetRequestTokenCredentials(callback, client):
    response, content = client.request('http://api.rdio.com/oauth/request_token', 'POST', urllib.urlencode({'oauth_callback':callback}))
    return dict(urlparse.parse_qsl(content)) 

def CreateLoginString(loginURL, oauthToken):
    return loginURL + "?oauth_token=" + oauthToken

def CreateRequestToken(oauthToken, oauthTokenSecret):
    return oauth.Token(oauthToken, oauthTokenSecret)

def GetAccessTokenCredentials(consumer, requestToken):
    # upgrade the request token to an access token
    client = oauth.Client(consumer, requestToken)
    response, content = client.request('http://api.rdio.com/oauth/access_token', 'POST')
    # return access token credentials
    return dict(urlparse.parse_qsl(content))

#Access Token Functions

def RdioGetCurrentUser(oauthToken, oauthTokenSecret, consumer):
    # Get current user information.
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)

    client = oauth.Client(consumer, accessToken)
    response, content = client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'currentUser'}))
    return json.loads(content)

def RdioCreatePlaylist(oauthToken, oauthTokenSecret, consumer, playlistInfo):
    #Create a playlist
    accessToken = oauth.Token(oauthToken, oauthTokenSecret)


    client = oauth.Client(consumer, accessToken)
    
    response, content = client.request('http://api.rdio.com/1/', 'POST', 
                                       urllib.urlencode({'method': 'createPlaylist', 
                                                         'name': playlistInfo['name'], 
                                                         'description': playlistInfo['description'], 
                                                         'tracks': playlistInfo['tracks'], 
                                                         'collaborationMode': RdioCollaborationModes['CollaborateAllUsers']}))

class RdioAuthenticator(object):
    """docstring for RdioAuthenticator"""
    
    consumer = None
    client = None

    def BuildConsumerAndClient(self, consumerKey, consumerSecret):
        # create the OAuth consumer credentials.
        self.consumer = oauth.Consumer(consumerKey, consumerSecret)

        # build client basked on consumer credentials. 
        self.client = oauth.Client(self.consumer)

# Make API request to add song to a playlist
def add(id):
    # response, content = client.request('http://api.rdio.com/1/', 'POST',
    #                                  urllib.urlencode({'method': 'get', 'keys': id}))

    # json_data = json.loads(content)

    # # TODO -- add to an Rdio playlist
    # return json.dumps(json_data['result'])
    pass
  
def newPlaylist(name):
    return 1

# Make API request to search for a song.
def search(query):
    # response, content = client.request('http://api.rdio.com/1/', 'POST', 
    #                                     urllib.urlencode({'method': 'search', 'query': query, 'types': 'Track'}))
    # # TODO: check the response
    # json_data = json.loads(content)
    # return json.dumps(json_data['result']['results'])
    pass
