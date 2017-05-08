# -*- coding: utf-8 -*-
from django.conf.urls import url
from guestbook.views import IndexView, SignView

app_name='guestbook'
urlpatterns = [
    url(r'^index/$',IndexView.as_view(), name='index'),
    url(r'^sign/$',SignView.as_view(), name='sign'),
]
