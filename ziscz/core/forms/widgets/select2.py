# coding=utf-8
from __future__ import unicode_literals

from django_select2.forms import ModelSelect2MultipleWidget

from ziscz.core.models import Person


class PersonMultipleSelectWidget(ModelSelect2MultipleWidget):
    model = Person
    search_fields = (
        'first_name__icontains',
        'last_name__icontains'
    )
