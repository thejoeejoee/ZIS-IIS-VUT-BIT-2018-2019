# coding=utf-8
from __future__ import unicode_literals

import json

from braces.views import UserFormKwargsMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, F
from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Person, TypeRole, Cleaning
from ziscz.core.utils.utils import get_object_or_none
from ziscz.core.views.delete import DeleteView
from ziscz.core.views.forms import SuccessMessageMixin, SaveAndContinueMixin
from ziscz.web.forms.person import PersonForm


class PersonListView(PermissionRequiredMixin, ListView):
    template_name = 'web/person_list.html'
    permission_required = 'core.view_person'

    queryset = Person.objects.select_related(
        'type_role',
        'user',
    ).prefetch_related(
        'trained_type_animals',
        'trained_type_enclosures',
    ).order_by(
        'type_role__order',
        'last_name',
        'first_name',
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


class PersonDetailView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin,
                       UserFormKwargsMixin, UpdateView):
    permission_required = 'core.view_person', 'core.edit_person'
    template_name = 'web/person_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    queryset = Person.objects.select_related('user')

    @atomic
    def form_valid(self, form):
        resp = super().form_valid(form)

        person = self.get_object()  # type: Person

        feedings_to_remove = person.feeding_executor.filter(
            date__gt=timezone.now(),
            done=False,
        ).exclude(
            feeding_animal_feeding__animal__type_animal__in=person.trained_type_animals.all(),
        )
        if feedings_to_remove.exists():
            messages.warning(
                self.request,
                ungettext(
                    'Following feeding was deleted due to person qualification lost: {}.',
                    'Following feedings were deleted due to person qualification lost: {}.',
                    feedings_to_remove.count(),
                ).format(', '.join(map(str, feedings_to_remove))),
            )
            feedings_to_remove.delete()

        person_cleanings_to_remove = person.cleaning_person_person.filter(
            cleaning__date__gt=timezone.now(),
            cleaning__done=False,
        ).exclude(
            cleaning__enclosure__type_enclosure__in=person.trained_type_enclosures.all(),
        )
        if person_cleanings_to_remove.exists():
            corresponding_cleanings = Cleaning.objects.filter(
                pk__in=person_cleanings_to_remove.values_list('cleaning__pk', flat=True)
            )
            messages.warning(
                self.request,
                ungettext(
                    'From following cleaning was deleted person assignment due to person qualification lost: {}.',
                    'From following cleanings were deleted person assignment due to person qualification lost: {}.',
                    corresponding_cleanings.count(),
                ).format(', '.join(map(str, corresponding_cleanings))),
            )
            person_cleanings_to_remove.delete()

            cleanings_to_remove = Cleaning.objects.annotate(
                cleaners_count=Count('cleaning_person_cleaning__person')
            ).filter(
                cleaners_count__lt=F('enclosure__min_cleaners_count')
            )
            if cleanings_to_remove.exists():
                messages.warning(
                    self.request,
                    ungettext(
                        'Following cleaning was deleted due to small executors count: {}.',
                        'Following cleanings were deleted due to small executors count: {}.',
                        cleanings_to_remove.count(),
                    ).format(', '.join(map(str, cleanings_to_remove))),
                )
                cleanings_to_remove.delete()
        return resp


class PersonCreateView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin,
                       UserFormKwargsMixin, CreateView):
    permission_required = 'core.view_person', 'core.add_person'
    template_name = 'web/form_detail.html'
    form_class = PersonForm
    success_url = reverse_lazy('person_list')
    model = Person

    def form_valid(self, form):
        resp = super(PersonCreateView, self).form_valid(form=form)
        password = get_user_model().objects.make_random_password()
        user = form.instance.user  # type: AbstractUser
        user.set_password(raw_password=password)
        user.save()
        messages.success(
            self.request,
            _('User was created, login credentials are {} {}.').format(user.username, password),
            extra_tags=json.dumps(dict(timeout=0, infinite=True))
        )
        return resp


class PersonDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'web/object_delete.html'
    success_url = reverse_lazy('person_list')
    model = Person
    permission_required = 'core.delete_person'

    @atomic
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if hasattr(obj, 'user'):
            obj.user.delete()
        return super().delete(request, *args, **kwargs)

    def can_perform_delete(self):
        obj = self.get_object() # type: Person
        if not hasattr(obj, 'user'):
            return True
        return obj.user != self.request.user