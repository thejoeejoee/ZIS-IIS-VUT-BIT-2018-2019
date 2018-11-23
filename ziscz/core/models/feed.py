# coding=utf-8
from django.db import models
from django.utils.formats import time_format, date_format
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _

from ziscz.core.models.managers.calendar import FeedingManager
from .base import BaseModel, BaseTypeModel, BaseEventModel


class TypeFeed(BaseTypeModel):
    pass


class Feeding(BaseEventModel):
    """
    Pravidlo pro krmení zvířat.
    """
    objects = FeedingManager()

    type_feed = models.ForeignKey(
        "core.TypeFeed",
        on_delete=models.PROTECT,
        related_name="feeding_feed_type"
    )

    animals = models.ManyToManyField(
        "core.Animal",
        through="core.FeedingAnimal"
    )

    executor = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="feeding_executor"
    )

    note = models.TextField(null=True, blank=True)

    amount = models.CharField(
        max_length=128,
        help_text=_('Amount of feed, etc. 1 kg, 1 l or 20 pieces.')
    )

    class Meta:
        ordering = 'date',

    def __str__(self):
        return _('Feeding at {} {}').format(
            time_format(localtime(self.date), use_l10n=True),
            date_format(self.date),
        )

    @property
    def specification(self):
        return _('{} by {} ({} {})').format(
            ', '.join(map(str, self.animals.all())),
            self.executor,
            self.type_feed,
            self.amount,
        )


class FeedingAnimal(BaseModel):
    """
    Krmená zvířata.
    """
    feeding = models.ForeignKey(
        "core.Feeding",
        on_delete=models.PROTECT,
        related_name="feeding_animal_feeding"
    )

    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="feeding_animal_animal"
    )

    class Meta:
        ordering = 'feeding__date',


__all__ = ["TypeFeed", "Feeding", "FeedingAnimal"]
