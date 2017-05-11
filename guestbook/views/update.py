# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from guestbook.forms import update
from guestbook.models import Greeting


class update(FormView):
	template_name = 'guestbook/update.html'
	form_class = update
	success_url = reverse_lazy('index')

	def get_guestbook_id(self):
		guestbook_id = self.request.GET.get('guestbook_id')
		return guestbook_id

	def get_guestbook_name(self):
		guestbook_name=self.request.GET.get('guestbook_name')
		return guestbook_name

	def get_content(self):
		content = self.request.GET.get('content')
		return content

	def get_context_data(self, **kwargs):
		guestbook_id=self.get_guestbook_id()
		guestbook_name=self.get_guestbook_name()
		content= self.get_content()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(update, self).get_context_data(**kwargs)
		context['update'] = form
		context['guestbook_id'] = guestbook_id
		context['guestbook_name'] = guestbook_name
		context['content'] = content
		return context

