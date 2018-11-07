# coding=utf-8
from __future__ import unicode_literals

from django.db import IntegrityError
from django.shortcuts import _get_queryset


def get_object_or_none(model_or_qs, **kwargs):
    qs = _get_queryset(model_or_qs)
    try:
        return qs.get(**kwargs)
    except (model_or_qs.DoesNotExist, ValueError, IntegrityError):
        return None
