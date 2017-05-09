# -*- coding: utf-8 -*-
from django.conf.urls import url
from guestbook.viewss import indexView,signView

app_name='guestbook'
urlpatterns = [
    url(r'^index/$',indexView.IndexView.as_view(), name='index'),
    url(r'^sign/$',signView.SignView.as_view(), name='sign'),
]
