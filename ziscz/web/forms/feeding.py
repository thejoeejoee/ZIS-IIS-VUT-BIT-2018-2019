# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row, Div
from django.forms import Textarea
from django.utils.translation import ugettext as _

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DateTimePickerInput
from ziscz.core.forms.widgets.select2 import PersonSelectWidget, AnimalMultipleSelectWidget
from ziscz.core.models import Feeding, Animal, FeedingAnimal
from ziscz.core.utils.m2m import update_m2m


class FeedingForm(BaseModelForm):
    class Meta:
        model = Feeding
        fields = (
            'type_feed',
            'animals',
            'executor',
            'date',
            'length',
            'note',
            'amount',
        )

        widgets = {
            'date': DateTimePickerInput(),
            'animals': AnimalMultipleSelectWidget(
                dependent_fields={
                    'executor': 'type_animal__person_type_animal_type_animal__person'
                }
            ),
            'note': Textarea(attrs=dict(rows=3)),
            'executor': PersonSelectWidget(),
        }
        help_texts = {
            'animals': _('Only animals, that could be feed by selected person, are displayed.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animals'].initial = Animal.objects.filter(feeding_animal_animal__feeding=self.instance)
        self.helper.layout = Layout(
            'executor',
            'animals',
            Row(
                Col('amount'),
                Col('type_feed')
            ),
            Row(
                Col('date'),
                Col('length'),
            ),
            'note',
            Div(css_id='feeding-planning'),
        )

    def clean(self):
        data = super().clean()

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
        return instance
