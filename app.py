#!usr/bin/python


# A simple-looking Python HTTP framework I just found
import web
from web import form


# Tells web.py where to look to find page templates
render = web.template.render('templates/');


# The form that allows users to search for songs
searchSongForm = form.Form(
  form.Textbox('song',
    form.notnull),
)


# The URL structure of the entire application.
# Syntax: 'regular expression', 'class to be called'
urls = (
  '/', 'index'
)


# Classes that handle URLs
class index:
  def GET(self):
    form = searchSongForm()
    return render.index(form)

  def POST(self):
    form = searchSongForm()
    if not form.validates():
      return render.index(form)
    else:
      return "Song requested: %s" % (form['song'].value)


# Initialize the application
if __name__ == "__main__":
  web.internalerror = web.debugerror
  app = web.application(urls, globals())
  app.run()