# -*- coding: utf-8 -*-
from google.appengine.api import mail


def send_email(sender, content):
	mail.send_mail(sender=sender,
       to="<tranngoc.uit@gmail.com>",
       subject=content,
       body=sender + content)
