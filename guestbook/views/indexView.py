# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from google.appengine.api import users
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME


class IndexView(TemplateView):
	template_name = 'guestbook/template.html'

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		if not guestbook_name or guestbook_name == '':
			guestbook_name = DEFAULT_GUESTBOOK_NAME
		return guestbook_name

	def get_context_data(self, **kwargs):
		guestbook_name = self.get_guestbook_name()
		greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)
		context = super(IndexView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['greetings_query'] = greetings_query
		context['greetings'] = greetings
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'
		context['url'] = url
		context['url_linktext'] = url_linktext
		return context
