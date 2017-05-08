from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from guestbook.forms import SignForm
from google.appengine.api import users
from django.core.urlresolvers import reverse_lazy
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse,HttpResponseRedirect
from google.appengine.ext import ndb
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
	@ndb.transactional
	def form_valid(self, form, **kwargs):
		# how to get velue in the form
		guestbook_name = form.cleaned_data['guestbook_name']
		content = form.cleaned_data['content']
		greeting = Greeting(parent=guestbook_key(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.guestbook_name = guestbook_name
		greeting.content = content
		greeting.put()
		return super(SignView, self).form_valid(form, **kwargs)

	def get_success_url(self):
		success_url = reverse_lazy('index')
		return '%s?guestbook_name=%s' % (success_url, self.get_guestbook_name())


	def send_email(self,request):
		subject = self.request.POST.get('subject','')
		message = self.request.POST.get('message','')
		from_email = self.request.POST.get('from_email','')
		if (subject and message and from_email):
			try:
				send_mail(subject, message, from_email,['tranngoc.uit@gmail.com'])
			except BadHeaderError:
				return HttpResponse('Invalid')
			return HttpResponseRedirect('guestbook/main_page')
		else:
			return HttpResponse("pls valid email")
