# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Person, TypeRole
from ziscz.core.utils.utils import get_object_or_none
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.person import PersonForm


class PersonListView(ListView):
    template_name = 'web/person_list.html'

    queryset = Person.objects.select_related(
        'type_role',
    ).prefetch_related(
        'trained_type_animals',
        'trained_type_enclosures',
    )

    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        # TODO: add filtration to template
        type_person = get_object_or_none(TypeRole, pk=self.request.GET.get('type_role'))
        if type_person:
            object_list = self.get_queryset().filter(type_person=type_person)

        data = super().get_context_data(object_list=object_list, **kwargs)
        data.update(dict(
            type_person_list=TypeRole.objects.all(),
            type_person=type_person,
        ))
        return data


class PersonDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/form_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    model = Person


class PersonCreateView(SuccessMessageMixin, CreateView):
    template_name = 'web/form_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    model = Person
