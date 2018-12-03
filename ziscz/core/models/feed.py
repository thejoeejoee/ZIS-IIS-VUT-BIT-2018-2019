# coding=utf-8
import typing
from typing import Iterable

from django.db import models
from django.utils.formats import time_format, date_format
from django.utils.timezone import localtime, localdate
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel, BaseTypeModel, BaseEventModel
from ..models.managers.calendar import FeedingQuerySet

if typing.TYPE_CHECKING:
    from . import Person


class TypeFeed(BaseTypeModel):
    class Meta(BaseTypeModel.Meta):
        verbose_name = _("Type feed")
        verbose_name_plural = _("Types feeding")


class Feeding(BaseEventModel):
    """
    Pravidlo pro krmení zvířat.
    """
    objects = FeedingQuerySet.as_manager()

    type_feed = models.ForeignKey(
        "core.TypeFeed",
        on_delete=models.PROTECT,
        related_name="feeding_feed_type",
        verbose_name=_('Type of feed'),
    )

    animals = models.ManyToManyField(
        "core.Animal",
        through="core.FeedingAnimal",
        verbose_name=_('Animals'),
    )

    executor = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="feeding_executor",
        verbose_name=_('Executor'),
    )

    note = models.TextField(null=True, blank=True, verbose_name=_('Note'), )

    amount = models.FloatField(
        help_text=_('Amount of feed.'),
        verbose_name=_('Amount'),
    )

    class Meta(BaseEventModel.Meta):
        verbose_name = _('Feeding')
        verbose_name_plural = _('Feedings')

    def __str__(self):
        return _('Feeding at {} {}').format(
            time_format(localtime(self.date)),
            date_format(localdate(self.date)),
        )

    @property
    def specification(self):
        return _('{} by {} ({} {})').format(
            ', '.join(map(str, self.animals.all())),
            self.executor,
            self.amount,
            self.type_feed,
        )

    @property
    def description(self):
        return ''

    def get_executors(self) -> Iterable["Person"]:
        return self.executor,

    @property
    def color(self):
        return '#b28704' if self.done else '#ffc107'


class FeedingAnimal(BaseModel):
    """
    Krmená zvířata.
    """
    feeding = models.ForeignKey(
        "core.Feeding",
        on_delete=models.CASCADE,
        related_name="feeding_animal_feeding"
    )

    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.CASCADE,
        related_name="feeding_animal_animal"
    )

    class Meta:
        ordering = 'feeding__date', 'animal'
        verbose_name = _('Feeding animal')
        verbose_name_plural = _('Feedings animal')


__all__ = ["TypeFeed", "Feeding", "FeedingAnimal"]
