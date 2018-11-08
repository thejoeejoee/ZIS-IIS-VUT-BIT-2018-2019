# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.models import Person


class PersonForm(BaseModelForm):
    class Meta:
        model = Person
        fields = (
            'type_role',
            'first_name',
            'last_name',
            'birth_date',
            'education',
            'note',
        )

        widgets = {
            'birth_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Col('first_name'),
                Col('last_name'),
            ),
            'type_role',
            'birth_date',
            Row(
                Col('education'),
                Col('note'),
            ),
        )

    def _save_m2m(self):
        pass

    def save(self, commit=True):
        instance = super().save(commit=commit)
        return instance

    def clean(self):
        return super().clean()
