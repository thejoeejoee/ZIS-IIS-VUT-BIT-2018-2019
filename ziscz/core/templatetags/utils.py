# coding=utf-8
from __future__ import unicode_literals

from typing import Type

from django import template
from django.db.models import Model

register = template.Library()


@register.filter
def get_verbose_name(model: Type[Model]):
    return model._meta.verbose_name.title()
