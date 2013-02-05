## Example Database created using the appengine datastore

import datetime
import webapp2

from google.appengine.ext import db

Class sick(db.Model):
	sickPerson = db.StringProperty()
	boss = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)