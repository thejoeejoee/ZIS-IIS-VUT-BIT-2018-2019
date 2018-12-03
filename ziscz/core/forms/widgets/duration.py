# coding=utf-8
from __future__ import unicode_literals

import json

from django.forms import TextInput
from django.utils.dateparse import parse_duration
from django.utils.translation import ugettext as _


class DurationPickerWidget(TextInput):
    class Media:
        js = (
            'core/duration-picker.js',
        )

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'data-duration-picker-widget': True,
            'data-trans': json.dumps({
                'day': _('day'),
                'hour': _('hour'),
                'minute': _('minute'),
                'second': _('second'),
                'days': _('days'),
                'hours': _('hours'),
                'minutes': _('minutes'),
                'seconds': _('seconds'),
            })
        })
        return attrs

    def format_value(self, value):
        # duration field formats value as duration string
        try:
            return str(parse_duration(value=str(value) if value else '').total_seconds())
        except AttributeError:
            return super().format_value(value=value)
