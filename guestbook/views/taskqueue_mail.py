# -*- coding: utf-8 -*-

from google.appengine.api import taskqueue
from guestbook.views import sendMail
import webapp2


def add_task(sender, content):
	task=taskqueue.add(
		url = '/sendemail',
		params = {'sender': sender, 'content': content},
		)


class task_handle_email(webapp2.RequestHandler):
	def post(self):
		sender=self.request.get('sender')
		content=self.request.get('content')
		sendMail.send_email(sender, content)


app = webapp2.WSGIApplication([
    ('/sendemail', task_handle_email)
], debug=True)
