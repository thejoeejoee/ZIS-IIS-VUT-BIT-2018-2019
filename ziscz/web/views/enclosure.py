# coding=utf-8
from __future__ import unicode_literals

import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ungettext
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Enclosure, Animal, AnimalStay
from ziscz.core.serializers import EnclosureSerializer
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.enclosure import EnclosureForm


class EnclosureListView(ListView):
    template_name = 'web/enclosure_list.html'
    queryset = Enclosure.objects.select_related(
        'type_enclosure',
    )
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['data'] = dict(
            enclosures=EnclosureSerializer(context.get('object_list'), many=True).data
        )
        return context


class EnclosureDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/enclosure_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure


class EnclosureCreateView(SuccessMessageMixin, CreateView):
    template_name = 'web/form_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure


class EnclosureAnimals(View):
    def post(self, request: WSGIRequest, *args, **kwargs):

        enclosures = json.loads(request.body.decode()).get('enclosures')
        moved = []

        for enclosure_data in enclosures:
            enclosure = get_object_or_404(Enclosure, pk=enclosure_data.get('id'))
            animals = Animal.live_animals.filter(
                pk__in=enclosure_data.get('animals')
            )

            for animal in animals:
                if animal.actual_enclosure != enclosure:
                    AnimalStay.objects.move_animal(
                        animal=animal,
                        new_enclosure=enclosure,
                    )
                    moved.append(animal)

        return JsonResponse(dict(
            success=True,
            msg=ungettext(
                'Animal {} was moved.',
                'Animals {} were moved.',
                len(moved)).format(''.join(map(str, moved)))
        ))
