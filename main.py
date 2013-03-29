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
import urllib
from datastore import Sick

from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.runtime import apiproxy_errors

from recaptcha.client import captcha
from os import environ


template_path = os.path.join(os.path.dirname(__file__),
                             'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        error_code = urllib.unquote(self.request.get('error'))
        sp_name = 'value="' + urllib.unquote(self.request.get('sn')) + '"'
        sp_email = 'value="' + urllib.unquote(self.request.get('se')) + '"'
        b_email = 'value="' + urllib.unquote(self.request.get('be')) + '"'
        chtml = captcha.displayhtml(
            public_key="6Lehdd4SAAAAAGyshD-jrfSNV1bV_InTDmtR62Sn",
            use_ssl=True,
            error=error_code)
        context = {'captchahtml': chtml, 'sp_name': sp_name, 'sp_email': sp_email, 'b_email': b_email}
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(context))


class SubmitHandler(webapp2.RequestHandler):
    def post(self):
        sick_person_name = self.request.get('sick_person_name')
        sick_person_email = self.request.get('sick_person_email')
        boss_email = self.request.get('boss_email')
        challenge = self.request.get('recaptcha_challenge_field')
        response = self.request.get('recaptcha_response_field')
        remote_ip = environ['REMOTE_ADDR']

        response = captcha.submit(recaptcha_challenge_field=challenge, recaptcha_response_field=response,
            private_key="6Lehdd4SAAAAAC0TKPW2gRxaly1HErcicR1Sck5P", remoteip=remote_ip)

        if response.is_valid:
            s = Sick(sick_person_name_ds=sick_person_name,
                sick_person_email_ds=sick_person_email,
                boss_email_ds=boss_email)

            q = db.Query(Sick).filter('sick_person_email_ds =',
                sick_person_email).order('-date_ds')

            result = q.get()
            s.put()
            if ((result is None) or (datetime.datetime.now() - result.date_ds) > datetime.timedelta(hours=8)):
                try:
                    mail.send_mail(sender="Don't Get Me Sick <dlorenc@dontgetmesick.com>",
                        to="%s <%s>" % (sick_person_name, sick_person_email),
                        subject="Don't Get Me Sick",
                        body="""Hello,
                            Coming to work sick is bad. We've heard that you're sick.
                            Your coworkers would appreciate it if you go home so you don't get them sick.

                            Thank you,
                            team@dontgetmesick.com""",
                        html="""<html><head></head><body>
                            <p>Hello,</p>
                            <p>Coming to work sick is bad. We've heard that you're sick.<br />
                            Your coworkers would appreciate it if you go home so you don't get them sick.</p>
                            <p>Thank you,<br />
                            team@dontgetmesick.com</p></body></html>""")
                    mail.send_mail(sender="Don't Get Me Sick <dlorenc@dontgetmesick.com>",
                        to="%s <%s>" % (boss_email, boss_email),
                        subject="Don't Get Me Sick",
                        body="""Hello,
                            Coming to work sick is bad. We've heard that one of your employees, %s is sick.
                            Some of %s's coworkers would appreciate it if you send %s home so no one else gets sick.

                            Thank you,
                            team@dontgetmesick.com""" % (sick_person_name, sick_person_name, sick_person_name),
                        html="""<html><head></head><body>
                            <p>Hello,</p>
                            <p>Coming to work sick is bad. We've heard that one of your employees, %s is sick.<br />
                            Some of %s's coworkers would appreciate it if you send %s home so no one else gets sick.</p>
                            <p>Thank you,<br />
                            team@dontgetmesickk.com</p></body></html>""" % (sick_person_name, sick_person_name, sick_person_name))
                    self.redirect('/success')
                except apiproxy_errors.OverQuotaError:
                    self.redirect('/overage')
            else:
                self.redirect('/already')
        else:
            redirect_string = '/?error=%s' % urllib.quote_plus(response.error_code)
            redirect_string += '&sn=%s' % urllib.quote_plus(sick_person_name)
            redirect_string += '&se=%s' % urllib.quote_plus(sick_person_email)
            redirect_string += '&be=%s' % urllib.quote_plus(boss_email)
            self.redirect(redirect_string)


class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('success.html')
        self.response.out.write(template.render(context))


class OverageHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('overage.html')
        self.response.out.write(template.render(context))


class AlreadyHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('already.html')
        self.response.out.write(template.render(context))


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render(context))


class ContactHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        template = jinja_environment.get_template('contact.html')
        self.response.out.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/success', SuccessHandler),
    ('/already', AlreadyHandler),
    ('/overage', OverageHandler),
    ('/about', AboutHandler),
    ('/contact', ContactHandler)
], debug=True)
