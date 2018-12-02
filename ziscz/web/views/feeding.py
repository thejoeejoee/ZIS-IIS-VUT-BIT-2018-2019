# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from ziscz.core.models import Feeding, Animal, Person
from ziscz.core.views.delete import DeleteView
from ziscz.core.views.forms import SuccessMessageMixin, SaveAndContinueMixin
from ziscz.web.forms.feeding import FeedingForm


class FeedingDetailView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, UpdateView):
    template_name = 'web/feeding_detail.html'
    form_class = FeedingForm
    success_url = reverse_lazy('calendar')
    model = Feeding
    permission_required = 'core.change_feeding'


class FeedingCreateView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, CreateView):
    template_name = 'web/feeding_detail.html'
    form_class = FeedingForm
    success_url = reverse_lazy('calendar')
    model = Feeding
    permission_required = 'core.add_feeding'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET.get('animal'):
            kwargs.setdefault('initial', dict()).update(dict(
                animals=get_list_or_404(Animal.live_animals, pk=self.request.GET.get('animal'))
            ))
        if self.request.GET.get('executor'):
            kwargs.setdefault('initial', dict()).update(dict(
                executor=get_object_or_404(Person, pk=self.request.GET.get('executor'))
            ))
        return kwargs


class FeedingDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'web/object_delete.html'
    success_url = reverse_lazy('calendar')
    model = Feeding
    permission_required = 'core.delete_feeding'
