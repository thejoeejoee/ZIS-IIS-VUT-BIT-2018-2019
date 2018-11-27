# coding=utf-8
from __future__ import unicode_literals

import json
from functools import partial
from operator import methodcaller
from typing import List

from django.forms import Field, TypedChoiceField, RadioSelect
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _


class DateRangeField(Field):
    """
    Date list range field, seconds are striped.
    """
    RANGE_KEY = 'range'

    def to_python(self, value) -> List[datetime]:
        if not value:
            return []
        data = json.loads(value)
        return list(
            map(
                methodcaller('replace', second=0, microsecond=0),
                map(
                    partial(
                        datetime.fromtimestamp,
                        tz=timezone.get_current_timezone()
                    ),
                    data.get(self.RANGE_KEY)
                )
            )
        )


class BooleanSwitchField(TypedChoiceField):
    widget = RadioSelect

    def __init__(self, empty_value='', **kwargs):
        super().__init__(coerce=lambda val: val == str(True), empty_value=empty_value, **kwargs)
        self.choices = (
            ("False", _('No')),
            ("True", _('Yes')),
        )
