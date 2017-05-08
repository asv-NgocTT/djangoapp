# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail,BadHeaderError
from django.views.generic import TemplateView, FormView
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import mail
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
from guestbook.forms import SignForm


class IndexView(TemplateView):
	template_name = 'guestbook/template.html'

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'
		context = super(IndexView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['greetings_query'] = greetings_query
		context['greetings'] = greetings
		context['url'] = url
		context['url_linktext'] = url_linktext
		return context


class SignView(FormView):
	template_name = 'guestbook/sign_page.html'
	form_class = SignForm
	success_url = reverse_lazy('index')

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		return guestbook_name

	def get_context_data(self, **kwargs):
		guestbook_name = self.get_guestbook_name()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(SignView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['sign_form'] = form
		return context

	def post(self, request, *args, **kwargs):
		# how to get a form in formview
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form, **kwargs)
		else:
			return self.form_invalid(form, **kwargs)


	def form_valid(self, form, **kwargs):
		# how to get velue in the form
		guestbook_name = form.cleaned_data['guestbook_name']
		content = form.cleaned_data['content']

		@ndb.transactional
		def functionput():
			greeting = Greeting(parent=guestbook_key(guestbook_name))
			if users.get_current_user():
				greeting.author = users.get_current_user()
			greeting.guestbook_name = guestbook_name
			greeting.content = content
			greeting.put()
		def email(guestbook_name):
			mail.send_mail(sender=guestbook_name,
			               to="<tranngoc.uit@gmail.com>",
			               subject=content,
			               body=guestbook_name + content)
		functionput()
		email(guestbook_name)
		return super(SignView, self).form_valid(form, **kwargs)


	def get_success_url(self):
		success_url = reverse_lazy('index')
		return '%s?guestbook_name=%s' % (success_url, self.get_guestbook_name())
