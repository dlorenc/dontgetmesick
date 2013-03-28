from google.appengine.ext import db


class Sick(db.Model):
    sick_person_email_ds = db.StringProperty(required=True)
    sick_person_name_ds = db.StringProperty(required=True)
    boss_email_ds = db.StringProperty(required=True)
    date_ds = db.DateTimeProperty(auto_now_add=True)
