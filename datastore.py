## Example Database created using the appengine datastore

import datetime
import webapp2

from google.appengine.ext import db

class Sick(db.Model):
    sick_person_email = db.EmailProperty(required=True)
    sick_person_name = db.StringProperty(required=True)
    boss_email = db.EmailProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
