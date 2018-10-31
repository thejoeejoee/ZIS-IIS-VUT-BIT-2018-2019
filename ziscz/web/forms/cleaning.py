# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row
from django.forms import Textarea
from django_select2.forms import Select2MultipleWidget

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.models import Cleaning, CleaningPerson, Person
from ziscz.core.utils.m2m import update_m2m


class CleaningForm(BaseModelForm):
    class Meta:
        model = Cleaning
        fields = (
            'enclosure',
            'date',
            'length',
            'note',
            'executors',
        )

        widgets = {
            'date': DatePickerInput(),
            'executors': Select2MultipleWidget(),
            'note': Textarea(attrs=dict(rows=3)),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'enclosure',
            'executors',
            Row(
                Col('date'),
                Col('length'),
            ),
            'note',
        )

    def _save_m2m(self):
        update_m2m(
            actual_objects=Person.objects.filter(cleaning_person_person__cleaning=self.instance),
            new_objects=self.cleaned_data.get('executors'),
            relation_model=CleaningPerson,
            static_field='cleaning',
            static_object=self.instance,
            dynamic_field='person',
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        return instance
