# coding=utf-8
from __future__ import unicode_literals

from braces.views import CsrfExemptMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.views import View
from rest_framework.generics import get_object_or_404

from ziscz.core.models import Cleaning, Feeding
from ziscz.core.templatetags.event import can_mark_as_done


class MarkAsDoneEventView(CsrfExemptMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        event = self.get_object()

        if can_mark_as_done(
                event=self.get_object(),
                user=self.request.user,
        ):
            event.done = True
            event.save(update_fields=['done'])
            messages.success(self.request, _('Event successfully marked as done.'))
        else:
            messages.warning(self.request, _('Event could not be marked as done.'))

        return HttpResponseRedirect(
            self.request.GET.get('next')
            if is_safe_url(self.request.GET.get('next'), None) else
            '/'
        )

    def get_object(self):
        try:
            return get_object_or_404(Cleaning, pk=self.kwargs.get('pk'))
        except Http404:
            return get_object_or_404(Feeding, pk=self.kwargs.get('pk'))
