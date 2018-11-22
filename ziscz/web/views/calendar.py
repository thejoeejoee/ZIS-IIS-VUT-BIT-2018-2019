# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView


class CalendarView(TemplateView):
    template_name = 'web/calendar.html'
