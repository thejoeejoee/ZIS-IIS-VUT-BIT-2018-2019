# coding=utf-8
from __future__ import unicode_literals

import json
from typing import Type, Any

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_verbose_name(model: Type[Model]):
    return model._meta.verbose_name.title()


@register.filter
def to_json(value: Any):
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder))
