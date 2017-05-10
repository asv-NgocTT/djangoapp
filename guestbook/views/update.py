# -*- coding: utf-8 -*-

from django.views.generic import FormView
from guestbook.forms import update
from guestbook.models import Greeting


class update(FormView):
	template_name = 'guestbook/update.html'
	form_class = update

	def get_guestbookid(self):
		guestbookid = self.request.GET.get('guestbookid')
		return guestbookid

	def get_guestbookname(self):
		guestbookname=self.request.GET.get('guestbookname')
		return guestbookname

	def get_context_data(self, **kwargs):
		guestbookid=self.get_guestbookid()
		guestbookname=self.get_guestbookname()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(update, self).get_context_data(**kwargs)
		context['guestbookid'] = guestbookid
		context['guestbookname'] = guestbookname
		context['form'] = form




