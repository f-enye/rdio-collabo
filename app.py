import sys              # For checking command-line arguments
import web              # A simple-looking Python HTTP framework I just found
import urllib           # Making POST requests to Rdio url
import json             # Parsing responses from Rdio API
import webservice
  
# The application requires that an Oauth key and secret be provided at the command line.
# Authentication is required in order to make API calls.
if len(sys.argv) < 4 :
  sys.exit("ERROR: Syntax: " + sys.argv[0] + " <port> <consumer_key> <consumer_secret>")


# Authenticate this application with Oauth
client = webservice.authenticate(sys.argv[2], sys.argv[3])


# The URL structure of the entire application.
# Syntax: 'regular expression', 'class to be called'
urls = (
  '/',            'index',
  '/search/(.+)', 'search'
)


# Tell web.py where to look to find page templates
render = web.template.render('templates/');


# Classes that handle URLs
class index:
  def GET(self):
    return render.index()

class search:
  def POST(self, query):
    response, content = client.request('http://api.rdio.com/1/', 'POST', 
                                       urllib.urlencode({'method': 'search', 'query': query, 'types': 'Track'}))
    # TODO: check the response
    json_data = json.loads(content)
    return json.dumps(json_data['result']['results'])


# Initialize the application
if __name__ == "__main__":
  web.internalerror = web.debugerror
  app = web.application(urls, globals())
  app.run()