# coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from ziscz.core.models import Cleaning, Enclosure, Person
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET.get('enclosure'):
            kwargs.setdefault('initial', dict()).update(dict(
                enclosure=get_object_or_404(Enclosure, pk=self.request.GET.get('enclosure'))
            ))
        if self.request.GET.get('executor'):
            kwargs.setdefault('initial', dict()).update(dict(
                executors=get_list_or_404(Person, pk=self.request.GET.get('executor'))
            ))
        return kwargs
