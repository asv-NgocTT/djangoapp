# -*- coding: utf-8 -*-
from django import forms


class SignForm(forms.Form):
    guestbook_name=forms.CharField(label='GuestBook Name')
    content=forms.CharField(label='Content', widget=forms.Textarea, max_length=10)
