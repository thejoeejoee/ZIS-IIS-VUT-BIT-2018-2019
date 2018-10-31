# coding=utf-8
from __future__ import unicode_literals

from django import template

from ziscz.core.utils.color import scale as scale_color

register = template.Library()


@register.filter
def scale(color: str, factor: float):
    return scale_color(color, factor)
