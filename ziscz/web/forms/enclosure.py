# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row
from django.forms import Textarea, NumberInput, IntegerField

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.duration import DurationPickerWidget
from ziscz.core.models import Enclosure


class EnclosureForm(BaseModelForm):
    min_cleaners_count = IntegerField(widget=NumberInput(attrs=dict(min=1)))

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
            'note': Textarea(attrs=dict(rows=3)),
            'min_cleaning_duration': DurationPickerWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'name',
            'type_enclosure',
            Row(
                Col('min_cleaning_duration'),
                Col('min_cleaners_count'),
            ),
            Row(
                Col('color'),
                Col('note'),
            ),
        )
        if not self.updating:
            self.fields['min_cleaners_count'].initial = 1

    def _save_m2m(self):
        pass
