# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Animal, TypeAnimal, AnimalStay, FeedingAnimal, Feeding
from ziscz.core.utils.utils import get_object_or_none
from ziscz.core.views.delete import DeleteView
from ziscz.core.views.forms import SuccessMessageMixin, SaveAndContinueMixin
from ziscz.web.forms.animal import AnimalForm


class AnimalListView(PermissionRequiredMixin, ListView):
    template_name = 'web/animal_list.html'
    allow_empty = True
    permission_required = 'core.view_animal'

    def get_queryset(self):
        return Animal.objects.prefetch_related(
            'animal_parent1',
            'animal_parent2',
            Prefetch(
                'animal_stay_animal',
                queryset=AnimalStay.objects.filter(AnimalStay.filter_for_actual()).select_related('enclosure'),
                to_attr='animal_stay_animal_actual'
            ),
        ).select_related(
            'type_animal',
            'parent1',
            'parent2',
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        type_animal = get_object_or_none(TypeAnimal, pk=self.request.GET.get('type_animal'))
        object_list = object_list or self.get_queryset()
        if type_animal:
            object_list = object_list.filter(type_animal=type_animal)

        dead_q = Animal.live_animals.get_dead_filter()
        data.update(dict(
            type_animal_list=TypeAnimal.objects.all(),
            type_animal=type_animal,
            object_list=object_list.filter(~dead_q),
            dead_animals=object_list.filter(dead_q),
        ))
        return data


class AnimalDetailView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, UpdateView):
    template_name = 'web/animal_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    permission_required = 'core.change_animal'

    def get_queryset(self):
        today = timezone.localdate()
        return Animal.objects.prefetch_related(
            'animal_stay_animal',
            'animal_stay_animal__enclosure',
        ).prefetch_related(
            # planned feedings, overriding property
            Prefetch(
                'feeding_animal_animal',
                queryset=FeedingAnimal.objects.filter(feeding__date__gte=today).select_related(
                    'feeding',
                    'feeding__type_feed',
                    'feeding__executor',
                ).order_by('-feeding__date'),
                to_attr='planned_feedings'
            )
        )


class AnimalCreateView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, CreateView):
    template_name = 'web/form_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    model = Animal
    permission_required = 'core.add_animal'


class AnimalDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'web/object_delete.html'
    success_url = reverse_lazy('animal_list')
    model = Animal
    permission_required = 'core.delete_animal'

    @atomic
    def delete(self, request, *args, **kwargs):
        feedings = tuple(Feeding.objects.filter(feeding_animal_feeding__animal=self.get_object()).values_list('id', flat=True))
        resp = super().delete(request, *args, **kwargs)
        Feeding.objects.filter(pk__in=feedings).filter(feeding_animal_feeding__isnull=True).delete()

        return resp
