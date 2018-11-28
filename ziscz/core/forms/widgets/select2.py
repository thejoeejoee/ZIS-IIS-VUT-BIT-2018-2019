# coding=utf-8
from __future__ import unicode_literals

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from ziscz.core.models import Person, Animal, Enclosure, TypeAnimal, TypeEnclosure


class PersonMultipleSelectWidget(ModelSelect2MultipleWidget):
    # TODO: order by role descendant
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

    def get_queryset(self):
        return self.model.live_animals.all()


class AnimalSelectWidget(ModelSelect2Widget):
    model = Animal
    search_fields = (
        'name__icontains',
        'type_animal__name__icontains',
    )


class TypeAnimalMultipleSelectWidget(ModelSelect2MultipleWidget):
    model = TypeAnimal
    search_fields = (
        'name__icontains',
    )


class TypeEnclosureMultipleSelectWidget(ModelSelect2MultipleWidget):
    model = TypeEnclosure
    search_fields = (
        'name__icontains',
    )
