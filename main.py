# -*- coding: utf-8 -*-

import os,sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

