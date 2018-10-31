# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row, Div
from django.forms import Textarea
from django.utils.translation import ugettext as _
from django_select2.forms import Select2MultipleWidget

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DateTimePickerInput
from ziscz.core.models import Cleaning, CleaningPerson, Person, Enclosure
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
            'date': DateTimePickerInput(),
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
            Div(css_id='cleaning-planning'),
        )

    def clean(self):
        data = super().clean()

        enclosure = data.get('enclosure')  # type: Enclosure
        if enclosure:
            if len(data.get('executors')) < enclosure.min_cleaners_count:
                self.add_error(
                    'executors',
                    _('Selected enclosure requires {} or more executors for cleaning.').format(
                        enclosure.min_cleaners_count
                    )
                )
            if data.get('length') < enclosure.min_cleaning_duration:
                self.add_error(
                    'length',
                    _('Selected enclosure require longer cleaning duration ({}) than filled.').format(
                        enclosure.min_cleaning_duration
                    )
                )
        return data

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
