# coding=utf-8
from __future__ import unicode_literals

from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from ziscz.core.templatetags.event import can_mark_as_done


class MarkAsDoneEventView(UserPassesTestMixin, CsrfExemptMixin, SingleObjectMixin, View):
    def test_func(self):
        can_mark_as_done()
