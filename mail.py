## Example handling of POST data from user input
import datetime
import timedelta
import webapp2
import datastore

from google.appengine.ext import db

class Mail(webapp.RequestHandler):
	def post(self):
		sickP = self.request.get('sickP')
		boss = self.request.get('boss')

		s = sick(sickPerson=Mail(user), sickPersonsBoss=Mail(boss))

		q = db.Query(sick).filter('sickperson=', sickP).order('-date')

		result = q.get()

		if (result == None):
			##automatically send email if no results
			s.put() ##put new entry in db

		elif ((result.date - datetime.now()) > timedelta (hours = 8)):
			##Send Email if the most recent entry is more than 8 hours old
			s.put() ##put new entry in db

		else:
			s.put() ##put new entry in db, optional
			##redirect to page saying email has already been sent