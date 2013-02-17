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
from datastore import Sick

from google.appengine.ext import db
from google.appengine.api import mail

template_path = os.path.join(os.path.dirname(__file__),
    'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(context))

##Handler for the mail requests
class MailHandler(webapp2.RequestHandler):
    def post(self):
        sick_person_name = self.request.get('sick_person_name')
        sick_person_email = self.request.get('sick_person_email')
        boss_email = self.request.get('boss_email')

        s = Sick(sick_person_name=sick_person_name,
                 sick_person_email=db.Email(sick_person_email),
                 boss_email=db.Email(boss_email))


        q = db.Query(Sick).filter('sick_person_email=',
            db.Email(sick_person_email)).order('-date')

        result = q.get()
        s.put()
        if (result == None):
            mail.send_mail(sender="Don't Get Me Sick <team@dontgetmesick.com>",
                to="%s <%s>" % (sick_person_name, sick_person_email),
                subject="Don't Get Me Sick",
                body="Hello,\n" +
                    "Coming to work sick is bad. We've heard that you're sick." +
                    "Your coworkers would appreciate it if you go home so" +
                    "you don't get them sick.\n\n" +
                    "Thank you,\n" +
                    "team@dontgetmesick.com")
            mail.send_mail(sender="Don't Get Me Sick <team@dontgetmesick.com>",
                to="%s <%s>" % (boss_email, boss_email),
                subject="Don't Get Me Sick",
                body="Hello,\n" +
                    "Coming to work sick is bad. We've heard that one of your" +
                    "employees, %s is sick" % sick_person_name +
                    "Some of %s's coworkers would appreciate it if you send" +
                    "%s home so no one else gets sick.\n\n" % sick_person_name +
                    "Thank you,\n") +
                    "team@dontgetmesick.com")
            self.redirect('/success')   ##redirect to success page

        elif ((result.date - datetime.datetime.now()) > datetime.timedelta(hours=8)):
            mail.send_mail(sender="Don't Get Me Sick <team@dontgetmesick.com>",
                to="%s <%s>" % (sick_person_name, sick_person_email),
                subject="Don't Get Me Sick",
                body="Hello,\n" +
                    "Coming to work sick is bad. We've heard that you're sick." +
                    "Your coworkers would appreciate it if you go home so" +
                    "you don't get them sick.\n\n" +
                    "Thank you,\n" +
                    "team@dontgetmesick.com")
            mail.send_mail(sender="Don't Get Me Sick <team@dontgetmesick.com>",
                to="%s <%s>" % (boss_email, boss_email),
                subject="Don't Get Me Sick",
                body="Hello,\n" +
                    "Coming to work sick is bad. We've heard that one of your" +
                    "employees, %s is sick" % sick_person_name +
                    "Some of %s's coworkers would appreciate it if you send" +
                    "%s home so no one else gets sick.\n\n" % sick_person_name +
                    "Thank you,\n") +
                    "team@dontgetmesick.com")
            self.redirect('/success')  ##redirect to success page

        else:
            self.redirect('/already')  ##redirect to a page saying an email has already been sent

##success page
class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('success.html')
        self.response.out.write(template.render(context))

##already page
class AlreadyHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('already.html')
        self.response.out.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', MailHandler),
    ('/success', SuccessHandler),
    ('/already', AlreadyHandler)
], debug=True)
