# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from ziscz.core.models import Cleaning
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.cleaning import CleaningForm


class CleaningDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/cleaning_detail.html'
    form_class = CleaningForm
    success_url = reverse_lazy('calendar')
    model = Cleaning


class CleaningCreateView(SuccessMessageMixin, CreateView):
    template_name = 'web/cleaning_detail.html'
    form_class = CleaningForm
    success_url = reverse_lazy('calendar')
    model = Cleaning
