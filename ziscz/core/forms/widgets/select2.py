# coding=utf-8
from __future__ import unicode_literals

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from ziscz.core.models import Person, Animal, Enclosure


class PersonMultipleSelectWidget(ModelSelect2MultipleWidget):
    model = Person
    search_fields = (
        'first_name__icontains',
        'last_name__icontains'
    )


class PersonSelectWidget(ModelSelect2Widget):
    model = Person
    search_fields = (
        'first_name__icontains',
        'last_name__icontains'
    )


class EnclosureSelectWidget(ModelSelect2Widget):
    model = Enclosure
    search_fields = (
        'name__icontains',
        'type_enclosure__name__icontains'
    )


class AnimalMultipleSelectWidget(ModelSelect2MultipleWidget):
    model = Animal
    search_fields = (
        'name__icontains',
        'type_animal__name__icontains',
    )
