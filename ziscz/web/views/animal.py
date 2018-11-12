# coding=utf-8
from __future__ import unicode_literals

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Animal, TypeAnimal, AnimalStay, Enclosure
from ziscz.core.utils.utils import get_object_or_none
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.animal import AnimalForm


class AnimalListView(ListView):
    template_name = 'web/animal_list.html'

    allow_empty = True

    def get_queryset(self):
        return Animal.objects.prefetch_related(
            'animal_parent1',
            'animal_parent2',
            # 'animal_stays__enclosure',
            Prefetch(
                'animal_stay_animal',
                queryset=AnimalStay.objects.filter(AnimalStay.filter_for_actual()),
            )
        ).select_related(
            'type_animal',
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        type_animal = get_object_or_none(TypeAnimal, pk=self.request.GET.get('type_animal'))
        if type_animal:
            object_list = self.get_queryset().filter(type_animal=type_animal)

        data = super().get_context_data(object_list=object_list, **kwargs)
        data.update(dict(
            type_animal_list=TypeAnimal.objects.all(),
            type_animal=type_animal,
        ))
        return data


class AnimalDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/animal_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    model = Animal


class AnimalCreateView(SuccessMessageMixin, CreateView):
    template_name = 'web/form_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    model = Animal
