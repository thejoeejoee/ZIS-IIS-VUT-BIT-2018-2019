# coding=utf-8
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Person, TypeRole
from ziscz.core.utils.utils import get_object_or_none
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.person import PersonForm


class PersonListView(PermissionRequiredMixin, ListView):
    template_name = 'web/person_list.html'
    permission_required = 'core.view_person'

    queryset = Person.objects.select_related(
        'type_role',
    ).prefetch_related(
        'trained_type_animals',
        'trained_type_enclosures',
    )

    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        type_person = get_object_or_none(TypeRole, pk=self.request.GET.get('type_role'))
        if type_person:
            object_list = self.get_queryset().filter(type_person=type_person)

        data = super().get_context_data(object_list=object_list, **kwargs)
        data.update(dict(
            type_person_list=TypeRole.objects.all(),
            type_person=type_person,
        ))
        return data


class PersonDetailView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'core.view_person', 'core.edit_person'
    template_name = 'web/person_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    model = Person


class PersonCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'core.view_person', 'core.add_person'
    template_name = 'web/form_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    model = Person

    def form_valid(self, form):
        super(PersonCreateView, self).form_valid(form=form)
        password = get_user_model().make_random_password()
        user = form.instance.user  # type: AbstractUser
        user.set_password(raw_password=password)
        messages.success(self.request, _('User was created, username is {}.').format(user.username))
