# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.models import Greeting, guestbook_key
from guestbook.forms import SignForm
from guestbook.views import taskqueue_mail


class SignView(FormView):
	template_name = 'guestbook/sign_page.html'
	form_class = SignForm
	success_url = reverse_lazy('index')

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name','')
		return guestbook_name

	def get_context_data(self, **kwargs):
		guestbook_name = self.get_guestbook_name()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(SignView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['sign_form'] = form
		return context

	def post(self, *args, **kwargs):
		# how to get a form in formview
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form, **kwargs)
		else:
			return self.form_invalid(form, **kwargs)

	def form_valid(self, form, **kwargs):
		# how to get values in the form
		guestbook_name = form.cleaned_data['guestbook_name']
		content = form.cleaned_data['content']
		greeting = Greeting(parent=guestbook_key(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.guestbook_name = guestbook_name
		greeting.content = content

		@ndb.transactional
		def functionput():
			greeting.put()
		if users.get_current_user():
			functionput()
		taskqueue_mail.add_task(greeting.author, content)
		return super(SignView, self).form_valid(form, **kwargs)

	def get_success_url(self):
		success_url = reverse_lazy('index')
		return '%s?guestbook_name=%s' % (success_url, self.get_guestbook_name())
