# -*- coding: utf-8 -*-

from django.conf.urls import url
from guestbook.views.signView import SignView
from guestbook.views.indexView import IndexView
from guestbook.views.update import update


app_name='guestbook'
urlpatterns = [
    url(r'^index/$',IndexView.as_view(), name='index'),
    url(r'^sign/$',SignView.as_view(), name='sign'),
	url(r'^update/$',update.as_view(), name='update'),
]
