# coding=utf-8
from django.db import models
from django.utils.formats import time_format, date_format
from django.utils.translation import ugettext as _

from .base import BaseModel, BaseTypeModel


class TypeFeed(BaseTypeModel):
    pass


class Feeding(BaseModel):
    """
    Pravidlo pro krmení zvířat.
    """
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

    date = models.DateTimeField()

    length = models.DurationField()

    done = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)

    amount = models.CharField(
        max_length=128,
        help_text=_('Amount of feed, etc. 1 kg, 1 l or 20 pieces.')
    )

    class Meta:
        ordering = 'date',

    def __str__(self):
        return _('Feeding at {} {}').format(
            time_format(self.date),
            date_format(self.date),
        )

    @property
    def specification(self):
        return _('Feed for {} at {} with {} ({}) by {}.').format(
            ', '.join(map(str, self.animals.all())),
            time_format(self.date),
            self.type_feed,
            self.amount,
            self.executor,
        )

    @property
    def start_date(self):
        return self.date.date()


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
