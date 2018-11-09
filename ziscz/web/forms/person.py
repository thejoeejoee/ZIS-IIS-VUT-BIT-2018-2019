# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row
from django.forms import Textarea

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.forms.widgets.select2 import TypeAnimalMultipleSelectWidget, TypeEnclosureMultipleSelectWidget
from ziscz.core.models import Person, PersonTypeEnclosure, TypeEnclosure, TypeAnimal, PersonTypeAnimal
from ziscz.core.utils.m2m import update_m2m


class PersonForm(BaseModelForm):
    class Meta:
        model = Person
        fields = (
            'type_role',
            'first_name',
            'last_name',
            'birth_date',
            'education',
            'note',
            'trained_type_animals',
            'trained_type_enclosures',
        )

        widgets = {
            'birth_date': DatePickerInput(),
            'trained_type_animals': TypeAnimalMultipleSelectWidget(),
            'trained_type_enclosures': TypeEnclosureMultipleSelectWidget(),
            'education': Textarea(attrs=dict(rows=3)),
            'note': Textarea(attrs=dict(rows=3)),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['trained_type_enclosures'].initial = TypeEnclosure.objects.filter(
            person_type_enclosure_type_enclosure__person=self.instance
        )

        self.fields['trained_type_animals'].initial = TypeAnimal.objects.filter(
            person_type_animal_type_animal__person=self.instance
        )

        self.helper.layout = Layout(
            Row(
                Col('first_name'),
                Col('last_name'),
            ),
            'type_role',
            'birth_date',
            'trained_type_animals',
            'trained_type_enclosures',
            Row(
                Col('education'),
                Col('note'),
            ),
        )

    def _save_m2m(self):
        update_m2m(
            actual_objects=self.fields['trained_type_enclosures'].initial,
            new_objects=self.cleaned_data.get('trained_type_enclosures'),
            relation_model=PersonTypeEnclosure,
            static_field='person',
            static_object=self.instance,
            dynamic_field='type_enclosure',
        )
        update_m2m(
            actual_objects=self.fields['trained_type_animals'].initial,
            new_objects=self.cleaned_data.get('trained_type_animals'),
            relation_model=PersonTypeAnimal,
            static_field='person',
            static_object=self.instance,
            dynamic_field='type_animal',
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        return instance

    def clean(self):
        return super().clean()
