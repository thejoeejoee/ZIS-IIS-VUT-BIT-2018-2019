# coding=utf-8
from __future__ import unicode_literals

from django.forms import TextInput


class DurationPickerWidget(TextInput):
    class Media:
        js = (
            'core/duration-picker.js',
        )

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'data-duration-picker-widget': True,
        })
        return attrs
