# coding=utf-8
from __future__ import unicode_literals

from django.forms import ModelForm

from ziscz.core.models import Animal


class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        fields = (
            'name',
            'type_animal',
        )
