#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import datetime
import timedelta
from datastore import sick

from google.appengine.ext import db

template_path = os.path.join(os.path.dirname(__file__),
    'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.out.write("Hello, world!")
        context = {}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(context))

##Handler for the mail requests
class MailHandler(webapp2.RequestHandler):
	def get(self):
		sickP = self.request.get('sickP')
		sickPName = self.request.get('sickPName')
		boss = self.request.get('boss')

		s = sick(sickPerson=Mail(sickP), sickPersonName=sickPName, sickPersonsBoss=Mail(boss))

		q = db.Query(sick).filter('sickPerson=', sickP).order('-date') ##might need to be Mail(sickP)

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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ('/submit', MailHandler)
], debug=True)
