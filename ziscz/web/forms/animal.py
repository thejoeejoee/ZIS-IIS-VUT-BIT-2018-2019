# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row
from django.forms import ModelChoiceField
from django_select2.forms import Select2MultipleWidget

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.models import Animal, AnimalRegion, Enclosure, AnimalStay, TypeRegion
from ziscz.core.utils.m2m import update_m2m


class AnimalForm(BaseModelForm):
    animal_stay = ModelChoiceField(queryset=Enclosure.objects.all(), required=False)

    class Meta:
        model = Animal
        fields = (
            'name',
            'type_animal',
            'birth_date',
            'origin_country',
            'occurrence_region',
            'death_date',

            'parent1',
            'parent2',
        )

        widgets = {
            'death_date': DatePickerInput(),
            'birth_date': DatePickerInput(),
            'occurrence_region': Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['occurrence_region'].required = False
        self.fields['animal_stay'].initial = self.instance.actual_enclosure

        self.helper.layout = Layout(
            'name',
            'type_animal',
            Row(
                Col('birth_date'),
                Col('death_date'),
            ),
            Row(
                Col('origin_country'),
                Col('occurrence_region'),
            ),
            Row(
                Col('parent1'),
                Col('parent2'),
            ),
            'animal_stay',
        )

        if self.updating:
            self.fields['parent1'].queryset = self.fields['parent2'].queryset = self.fields['parent1'].queryset.filter(
                type_animal=self.instance.type_animal
            ).exclude(pk=self.instance.pk)

    def _save_m2m(self):
        update_m2m(
            actual_objects=TypeRegion.objects.filter(animal_region_region__animal=self.instance),
            new_objects=self.cleaned_data.get('occurrence_region'),
            relation_model=AnimalRegion,
            static_field='animal',
            static_object=self.instance,
            dynamic_field='region',
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if 'animal_stay' in self.changed_data:
            AnimalStay.objects.move_animal(
                animal=self.instance,
                new_enclosure=self.cleaned_data.get('animal_stay'),
            )
        return instance

    def clean(self):
        # TODO: animal parent validation
        return super().clean()
