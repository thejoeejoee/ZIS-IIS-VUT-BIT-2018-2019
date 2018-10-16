# coding=utf-8
from __future__ import unicode_literals

from bootstrap_datepicker_plus import DatePickerInput as BsDatePickerInput
from django.conf import settings


class DatePickerInput(BsDatePickerInput):
    options = dict(
        locale=settings.LANGUAGE_CODE,
    )
    format = '%d. %m. %Y'
