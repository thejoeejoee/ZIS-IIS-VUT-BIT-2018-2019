# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from ziscz.core.models import Feeding
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.feeding import FeedingForm


class FeedingDetailView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'web/form_detail.html'
    form_class = FeedingForm
    success_url = reverse_lazy('calendar')
    model = Feeding
    permission_required = 'core.change_feeding'


class FeedingCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'web/feeding_detail.html'
    form_class = FeedingForm
    success_url = reverse_lazy('calendar')
    model = Feeding
    permission_required = 'core.create_feeding'
