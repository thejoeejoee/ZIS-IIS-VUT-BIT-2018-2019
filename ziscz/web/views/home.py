# coding=utf-8
from __future__ import unicode_literals

from operator import attrgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView

from ziscz.core.models import Cleaning, Feeding


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        person = None
        if hasattr(self.request.user, 'person_user'):
            person = self.request.user.person_user

        if person and self.request.user.has_perms(('core.change_cleaning', 'core.change_feeding')):
            q_cleaning = Cleaning.objects.person_q(person=person)
            q_feeding = Feeding.objects.person_q(person=person)
        else:
            q_cleaning, q_feeding = Q(), Q()

        data.update(
            # actual_cleanings=Cleaning.objects.current(),
            # actual_feedings=Feeding.objects.current(),
            today_events=sorted(
                tuple(
                    Cleaning.objects.in_date().filter(q_cleaning)
                ) + tuple(
                    Feeding.objects.in_date().filter(q_feeding)
                ),
                key=attrgetter('date')
            ),
            now=timezone.now(),
        )

        return data


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = 'web/help.html'


class CreditsView(LoginRequiredMixin, TemplateView):
    template_name = 'web/credits.html'
