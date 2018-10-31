# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from ziscz.core.models import Animal, Enclosure
from ziscz.core.serializers import EnclosureSerializer
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.animal import AnimalForm


class AnimalListView(ListView):
    template_name = 'web/animal_list.html'
    model = Animal
    allow_empty = True


class EnclosureListView(ListView):
    template_name = 'web/enclosure_list.html'
    model = Enclosure
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['data'] = dict(
            enclosures=EnclosureSerializer(context.get('object_list'), many=True).data
        )
        return context


class AnimalDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/animal_detail.html'
    form_class = AnimalForm
    success_url = reverse_lazy('animal_list')
    model = Animal
