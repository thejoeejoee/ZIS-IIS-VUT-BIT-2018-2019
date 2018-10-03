# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _
from .base import BaseTypeModel


class TypeRegion(BaseTypeModel):
    pass


class TypeCountry(BaseTypeModel):
    pass

__all__ = ["TypeCountry", "TypeCountry"]