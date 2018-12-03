# coding=utf-8
from __future__ import unicode_literals

from datetime import timedelta
from typing import Iterable, Optional
from uuid import UUID

from crispy_forms.layout import Layout, Row, Div, HTML
from django.db.transaction import atomic
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.fields import DateRangeField, BooleanSwitchField
from ziscz.core.forms.widgets.datepicker import DateTimePickerInput
from ziscz.core.forms.widgets.duration import DurationPickerWidget
from ziscz.core.forms.widgets.select2 import PersonMultipleSelectWidget, EnclosureSelectWidget
from ziscz.core.models import Cleaning, CleaningPerson, Person, Enclosure
from ziscz.core.utils.m2m import update_m2m


class CleaningForm(BaseModelForm):
    date_range = DateRangeField(required=False)
    done = BooleanSwitchField(required=False, label=_('Done'))

    class Meta:
        model = Cleaning
        fields = (
            'enclosure',
            'length',
            'note',
            'executors',
            'date',
            'done',
        )

        widgets = {
            'enclosure': EnclosureSelectWidget(),
            'executors': PersonMultipleSelectWidget(dependent_fields={
                # all persons qualified to clean selected enclosure
                'enclosure': 'person_type_enclosure_person__type_enclosure__enclosure_type_enclosure'
            }),
            'note': Textarea(attrs=dict(rows=2)),
            'length': DurationPickerWidget(),
            'date': DateTimePickerInput(),
        }

        help_texts = {
            'executors': _('Displayed are only persons that are able to clean selected enclosure.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filled by range
        if not self.updating:
            self.fields['date'].required = False
            self.fields['date'].disabled = True

        self.helper.layout = Layout(
            'enclosure',
            'executors',
            Row(
                Col('length'),
                Col('note'),
                Col('done') if self.updating else None,
            ),
            Div(
                HTML(render_to_string('web/range_planning_note.html')),
                Div(css_id='cleaning-planning')
            ) if not self.updating else 'date',
        )
        if self.instance.done:
            for f in ('date', 'length', 'executors', 'enclosure'):
                self.fields[f].disabled = True

        enclosure = self.fields['enclosure'].initial or (
            Enclosure.objects.filter(
                pk=self.initial.get('enclosure')
            ).first()
            if isinstance(self.initial.get('enclosure'), UUID)
            else self.initial.get('enclosure')
        )  # type: Optional[Enclosure]

        if enclosure:
            self.fields['length'].initial = enclosure.min_cleaning_duration.total_seconds()

    def clean(self):
        data = super().clean()

        enclosure = data.get('enclosure')  # type: Enclosure
        executors = data.get('executors', ())  # type: Iterable[Person]
        if enclosure:
            if len(executors) < enclosure.min_cleaners_count:
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
        else:
            date_range = list(filter(None, (data.get('date'), )))

        length = data.get('length')  # type: Optional[timedelta]

        if date_range and length:
            for date in date_range:
                for executor in executors:
                    feeding, cleaning = executor.find_in_time(
                        start=date,
                        length=length
                    )
                    if feeding.exclude(pk=self.instance.pk).exists() or cleaning.exclude(pk=self.instance.pk).exists():
                        self.add_error(
                            'executors',
                            _('Executor {} has not time in filled date and duration - he has {}.').format(
                                executor,
                                ', '.join(
                                    filter(
                                        None,
                                        map(
                                            ','.join,
                                            (
                                                map(str, feeding),
                                                map(str, cleaning),
                                            )
                                        )
                                    )
                                )
                            )
                        )
                        break
        if not date_range:
            self.add_error(None, _('Please, specify datetime to plan.'))

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

        if self.updating:
            pass
        else:
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
