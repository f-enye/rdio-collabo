"""
webservice

This module is an interface to an external music API.
"""

import oauth2 as oauth  # Oauth stuff for authentication
import urllib, cgi      # Making POST requests to url
import json             # Parsing responses from API

client = None           # An authorized Oauth client for making API requests

# Authenticate with OAuth
def authenticate(CONSUMER_KEY, CONSUMER_SECRET):
    # The following authentication routine courtesy Rdio documentation.

    global client

    # create the OAuth consumer credentials
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # make the initial request for the request token
    client = oauth.Client(consumer)
    # response, content = client.request('http://api.rdio.com/oauth/request_token', 'POST', urllib.urlencode({'oauth_callback':'oob'}))
    # parsed_content = dict(cgi.parse_qsl(content))
    # request_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])

    # # ask the user to authorize this application
    # print 'Just gotta get you signed in to Rdio real quick: %s?oauth_token=%s' % (parsed_content['login_url'], parsed_content['oauth_token'])
    # oauth_verifier = raw_input('Enter the PIN / OAuth verifier: ').strip()
    # # associate the verifier with the request token
    # request_token.set_verifier(oauth_verifier)

    # # upgrade the request token to an access token
    # client = oauth.Client(consumer, request_token)
    # response, content = client.request('http://api.rdio.com/oauth/access_token', 'POST')
    # parsed_content = dict(cgi.parse_qsl(content))
    # access_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])

    # # make an authenticated API call
    # client = oauth.Client(consumer, access_token)
    # response = client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'currentUser'}))

# Make API request to add song to a playlist
def add(id):
    response, content = client.request('http://api.rdio.com/1/', 'POST',
                                     urllib.urlencode({'method': 'get', 'keys': id}))

    json_data = json.loads(content)

    # TODO -- add to an Rdio playlist
    return json.dumps(json_data['result'])
  
def newPlaylist(name):
    return 1

# Make API request to search for a song.
def search(query):
    response, content = client.request('http://api.rdio.com/1/', 'POST', 
                                        urllib.urlencode({'method': 'search', 'query': query, 'types': 'Track'}))
    # TODO: check the response
    json_data = json.loads(content)
    return json.dumps(json_data['result']['results'])
