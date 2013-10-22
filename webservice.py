"""
webservice

This module is an interface to an external music API.
"""

import oauth2 as oauth  # Oauth stuff for authentication

# Authenticate with OAuth
def authenticate(consumer_key, consumer_secret):
  consumer = oauth.Consumer(consumer_key, consumer_secret)
  return oauth.Client(consumer)
