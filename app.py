"""
app

This is the application's main module.
"""

import sys              # For checking command-line arguments
import web              # A simple-looking Python HTTP framework I just found
import webservice       # An interface to an external music API.
import data
  
# The application requires Oauth authentication in order to make API calls.
if len(sys.argv) < 4 :
    sys.exit("ERROR: Syntax: " + sys.argv[0] + " <port> <consumer_key> <consumer_secret>")
webservice.authenticate(sys.argv[2], sys.argv[3])

# The URL structure of the entire application.
# A feature of the web.py framework.
# Syntax: 'regular expression', 'class to be called'
urls = (
    '/',                  'index',
    '/add/(.+)',          'add',
    '/playlists/new/(.+)', 'new_playlist',
    '/playlists/nearby',  'nearby_playlist',
    '/search/(.+)',       'search'
)

# Tell web.py where to look to find page templates
render = web.template.render('templates/')

# Classes that handle URLs
class index:
    def GET(self):
        return render.index()

class new_playlist:
    def POST(self, name):
        webservice.newPlaylist(name)
        data.newPlaylist(name)
        return render.playlist(name)

class nearby_playlist:
  def POST(self):
    return data.nearby()

class add:
    def POST(self, id):
        return webservice.add(id)

class search:
    def POST(self, query):
        return webservice.search(query)


# Initialize the application
if __name__ == "__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()
