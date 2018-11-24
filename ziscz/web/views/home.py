# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ziscz.core.models import Cleaning, Feeding


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data.update(
            actual_cleanings=Cleaning.objects.current(),
            actual_feedings=Feeding.objects.current(),
        )

        return data


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = 'web/help.html'


class CreditsView(LoginRequiredMixin, TemplateView):
    template_name = 'web/credits.html'
