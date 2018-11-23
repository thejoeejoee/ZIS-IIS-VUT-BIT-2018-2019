# coding=utf-8
from __future__ import unicode_literals

import json
from functools import partial
from operator import methodcaller
from typing import List

from django.forms import Field
from django.utils import timezone
from django.utils.datetime_safe import datetime


class DateRangeField(Field):
    """
    Date list range field, seconds are striped.
    """
    RANGE_KEY = 'range'

    def to_python(self, value) -> List[datetime]:
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
