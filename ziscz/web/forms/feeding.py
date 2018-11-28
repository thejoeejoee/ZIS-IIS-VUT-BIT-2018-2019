# coding=utf-8
from __future__ import unicode_literals

from datetime import timedelta
from typing import Optional

from crispy_forms.layout import Layout, Row, Div, HTML
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.fields import DateRangeField, BooleanSwitchField
from ziscz.core.forms.widgets.datepicker import DateTimePickerInput
from ziscz.core.forms.widgets.duration import DurationPickerWidget
from ziscz.core.forms.widgets.select2 import PersonSelectWidget, AnimalMultipleSelectWidget
from ziscz.core.models import Feeding, Animal, FeedingAnimal, Person
from ziscz.core.utils.m2m import update_m2m


class FeedingForm(BaseModelForm):
    date_range = DateRangeField(required=False)
    done = BooleanSwitchField(required=False)

    class Meta:
        model = Feeding
        fields = (
            'type_feed',
            'animals',
            'executor',
            'length',
            'note',
            'amount',
            'date',
            'done',
        )

        widgets = {
            'animals': AnimalMultipleSelectWidget(
                dependent_fields={
                    'executor': 'type_animal__person_type_animal_type_animal__person'
                }
            ),
            'note': Textarea(attrs=dict(rows=2)),
            'executor': PersonSelectWidget(),
            'length': DurationPickerWidget(),
            'date': DateTimePickerInput(),
        }
        help_texts = {
            'animals': _('Only live animals, that could be feed by selected person, are displayed.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.updating:
            self.fields['date'].required = False
            self.fields['date'].disabled = True

        self.fields['animals'].initial = Animal.objects.filter(feeding_animal_animal__feeding=self.instance)
        self.helper.layout = Layout(
            'executor',
            'animals',
            Row(
                Col('amount'),
                Col('type_feed')
            ),
            Row(
                Col('length'),
                Col('note'),
                Col('done') if self.updating else None,
            ),
            Div(
                HTML(render_to_string('web/cleaning_planning_note.html')),
                Div(css_id='feeding-planning')
            ) if not self.updating else 'date',
        )

        if self.instance.done:
            for f in ('executor', 'animals', 'amount', 'type_feed', 'length', 'date'):
                self.fields[f].disabled = True

        self.fields['animals'].queryset = Animal.live_animals.all()

    def clean(self):
        data = super().clean()

        date_range = data.get('date_range')
        if date_range:
            self.instance.date = data['date'] = date_range[0]
        else:
            date_range = [data.get('date')]

        executor = data.get('executor')  # type: Optional[Person]
        length = data.get('length')  # type: Optional[timedelta]

        if executor and date_range and length:
            for date in date_range:
                feeding, cleaning = executor.find_in_time(
                    start=date,
                    length=length
                )
                if feeding.exclude(pk=self.instance.pk).exists() or cleaning.exclude(pk=self.instance.pk).exists():
                    self.add_error(
                        'executor',
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

        return data

    def _save_m2m(self):
        update_m2m(
            actual_objects=self.fields['animals'].initial,
            new_objects=self.cleaned_data.get('animals'),
            relation_model=FeedingAnimal,
            static_field='feeding',
            static_object=self.instance,
            dynamic_field='animal',
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if not self.updating:
            date_range = self.cleaned_data.get('date_range')
            for date in date_range[1:]:
                # skip first
                feeding = Feeding(
                    type_feed=instance.type_feed,
                    executor=instance.executor,
                    note=instance.note,
                    amount=instance.amount,
                    length=instance.length,
                    date=date,
                )
                feeding.save()
                for animal in self.cleaned_data.get('animals'):
                    FeedingAnimal.objects.create(
                        feeding=feeding,
                        animal=animal,
                    )

        return instance
