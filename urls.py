# -*- coding: utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('guestbook.urls')),
    ]
