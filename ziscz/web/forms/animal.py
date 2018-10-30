# coding=utf-8
from __future__ import unicode_literals

from django.forms import ModelForm, ModelChoiceField
from django_select2.forms import Select2MultipleWidget

from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.models import Animal, AnimalRegion, Enclosure, AnimalStay
from ziscz.core.models.region import TypeRegion
from ziscz.core.utils.m2m import update_m2m


class AnimalForm(ModelForm):
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
