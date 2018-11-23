# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView


class CalendarView(PermissionRequiredMixin, TemplateView):
    template_name = 'web/calendar.html'
    permission_required = 'core.view_cleaning', 'core.view_feeding'
