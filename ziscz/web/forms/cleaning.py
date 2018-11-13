# coding=utf-8
from __future__ import unicode_literals

from typing import Optional

from crispy_forms.layout import Layout, Row, Div, HTML
from django.db.transaction import atomic
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.fields import DateRangeField
from ziscz.core.forms.widgets.select2 import PersonMultipleSelectWidget, EnclosureSelectWidget
from ziscz.core.models import Cleaning, CleaningPerson, Person, Enclosure
from ziscz.core.utils.m2m import update_m2m


class CleaningForm(BaseModelForm):
    date_range = DateRangeField(required=False)

    class Meta:
        model = Cleaning
        fields = (
            'enclosure',
            'length',
            'note',
            'executors',
            'date',
        )

        widgets = {
            'enclosure': EnclosureSelectWidget(),
            'executors': PersonMultipleSelectWidget(dependent_fields={
                # all persons qualified to clean selected enclosure
                'enclosure': 'person_type_enclosure_person__type_enclosure__enclosure_type_enclosure'
            }),
            'note': Textarea(attrs=dict(rows=2)),
        }

        help_texts = {
            'executors': _('Displayed are only persons that are able to clean selected enclosure.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filled by range
        self.fields['date'].required = False
        self.helper.layout = Layout(
            'enclosure',
            'executors',
            Row(
                Col('length'),
                Col('note'),
            ),
            HTML(render_to_string('web/cleaning_planning_note.html')),
            Div(css_id='cleaning-planning') if not self.updating else Div(),
        )

        enclosure = self.fields['enclosure'].initial or self.initial.get('enclosure')  # type: Optional[Enclosure]
        if enclosure:
            self.initial.update(dict(
                length=enclosure.min_cleaning_duration,
            ))

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
            length = data.get('length')
            if length and length < enclosure.min_cleaning_duration:
                self.add_error(
                    'length',
                    _('Selected enclosure require longer cleaning duration ({}) than filled.').format(
                        enclosure.min_cleaning_duration
                    )
                )

        date_range = data.get('date_range')
        if date_range:
            self.instance.date = data['date'] = date_range[0]

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

    @atomic
    def save(self, commit=True):
        instance = super().save(commit=commit)

        if not self.updating:
            date_range = self.cleaned_data.get('date_range')
            for date in date_range[1:]:
                # skip first
                cleaning = Cleaning(
                    enclosure=instance.enclosure,
                    length=instance.length,
                    note=instance.note,
                    date=date,
                )
                cleaning.save()
                for person in self.cleaned_data.get('executors'):
                    CleaningPerson.objects.create(
                        cleaning=cleaning,
                        person=person,
                    )

        return instance
