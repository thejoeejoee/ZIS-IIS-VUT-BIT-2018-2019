# coding=utf-8
from django.utils.translation import ugettext as _

from .base import BaseTypeModel


class TypeRegion(BaseTypeModel):
    """
    Oblast výskytu.
    """

    class Meta(BaseTypeModel.Meta):
        verbose_name = _('Type region')
        verbose_name_plural = _('Types region')


class TypeCountry(BaseTypeModel):
    """
    Země pro původ zvířat.
    """

    class Meta(BaseTypeModel.Meta):
        verbose_name = _('Type country')
        verbose_name_plural = _('Types country')


__all__ = ["TypeCountry", "TypeRegion"]
