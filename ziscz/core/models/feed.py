# coding=utf-8
from django.db import models

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


__all__ = ["TypeFeed", "Feeding", "FeedingAnimal"]
