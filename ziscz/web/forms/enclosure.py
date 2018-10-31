# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row, Div
from django.forms import ModelMultipleChoiceField, Textarea

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.select2 import PersonMultipleSelectWidget
from ziscz.core.models import Enclosure, Person, EnclosurePerson
from ziscz.core.utils.m2m import update_m2m


class EnclosureForm(BaseModelForm):
    trained_persons = ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=PersonMultipleSelectWidget,
        required=False,
    )

    class Meta:
        model = Enclosure
        fields = (
            'name',
            'type_enclosure',
            'min_cleaning_duration',
            'min_cleaners_count',
            'color',
            'note',
        )

        widgets = {
            'note': Textarea(attrs=dict(rows=5))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trained_persons'].initial = Person.objects.filter(enclosure_person_person__enclosure=self.instance)

        self.helper.layout = Layout(
            'name',
            'type_enclosure',
            'trained_persons',
            Row(
                Col('min_cleaning_duration'),
                Col('min_cleaners_count'),
            ),
            Row(
                Col('color'),
                Col('note'),
            ),
        )

    def _save_m2m(self):
        update_m2m(
            actual_objects=Person.objects.filter(enclosure_person_person__enclosure=self.instance),
            new_objects=self.cleaned_data.get('trained_persons'),
            relation_model=EnclosurePerson,
            static_field='enclosure',
            static_object=self.instance,
            dynamic_field='person',
        )
