# coding=utf-8
from __future__ import unicode_literals

from bootstrap_datepicker_plus import DatePickerInput
from django.forms import ModelForm

from ziscz.core.models import Animal


class AnimalForm(ModelForm):
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
            # TODO: fix missing jQ in webpack bundle
            'death_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            'birth_date': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
        }

    def _save_m2m(self):
        # TODO: save custom m2m
        pass