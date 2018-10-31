# coding=utf-8
from __future__ import unicode_literals

from operator import attrgetter

from django.views.generic import TemplateView

from ziscz.core.models import Cleaning, Feeding


class CalendarView(TemplateView):
    template_name = 'web/calendar.html'

    def get_context_data(self, **kwargs):
        events = tuple(
            Cleaning.objects.all()
        ) + tuple(
            Feeding.objects.all()
        )
        return dict(
            events=sorted(events, key=attrgetter('date'))
        )
