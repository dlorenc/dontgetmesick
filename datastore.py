## Example Database created using the appengine datastore

import datetime
import webapp2

from google.appengine.ext import db

Class sick(db.Model):
	sickPerson = db.EmailProperty(required=True)
	sickPersonsBoss = db.EmailProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)