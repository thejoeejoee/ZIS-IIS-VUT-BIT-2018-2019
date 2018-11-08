# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'web/home.html'


class HelpView(TemplateView):
    template_name = 'web/help.html'
