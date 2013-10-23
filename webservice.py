"""
webservice

This module is an interface to an external music API.
"""

import oauth2 as oauth  # Oauth stuff for authentication
import urllib           # Making POST requests to url
import json             # Parsing responses from API

client = None           # An authorized Oauth client for making API requests

# Authenticate with OAuth
def authenticate(consumer_key, consumer_secret):
  global client
  consumer = oauth.Consumer(consumer_key, consumer_secret)
  client = oauth.Client(consumer)

# Make API request to add song to a playlist
def add(id):
  # TODO
  return 1
  
# Make API request to search for a song.
def search(query):
  response, content = client.request('http://api.rdio.com/1/', 'POST', 
                                     urllib.urlencode({'method': 'search', 'query': query, 'types': 'Track'}))
  # TODO: check the response
  json_data = json.loads(content)
  return json.dumps(json_data['result']['results'])
