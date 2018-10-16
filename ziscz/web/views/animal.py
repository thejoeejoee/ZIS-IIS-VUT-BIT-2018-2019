# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from ziscz.core.models import Animal
from ziscz.web.forms.animal import AnimalForm


class AnimalListView(ListView):
    template_name = 'web/animal_list.html'
    model = Animal
    allow_empty = True


class AnimalDetailView(UpdateView):
    template_name = 'web/animal_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    model = Animal