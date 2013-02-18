from google.appengine.ext import db


class Sick(db.Model):
    sick_person_email = db.StringProperty(required=True)
    sick_person_name = db.StringProperty(required=True)
    boss_email = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
