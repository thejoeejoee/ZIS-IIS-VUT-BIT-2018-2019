# coding=utf-8
from django.db import models
from .base import BaseModel, BaseTypeModel


class TypeFeed(BaseTypeModel):
    pass


class FeedingRule(BaseModel):
    feed_type = models.ForeignKey(
        "core.TypeFeed",
        on_delete=models.PROTECT,
        related_name="feeding_rule_feed_type"
    )

    weight = models.PositiveIntegerField()

    periodicity = models.ForeignKey(
        "core.Periodicity",
        on_delete=models.PROTECT,
        related_name="feeding_rule_periodicity"
    )

    feeded_animals = models.ManyToManyField(
        "core.Animal",
        through="core.FeedingRuleAnimal"
    )

    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)


class Feeding(BaseModel):
    rule = models.ForeignKey(
        "core.FeedingRule",
        on_delete=models.PROTECT,
        related_name="feeding_rule"
    )

    executor = models.ForeignKey(
        "core.Person",
        null=True,
        on_delete=models.PROTECT,
        related_name="feeding_executor"
    )

class FeedingRuleAnimal(BaseModel):
    feeding_rule = models.ForeignKey(
        "core.FeedingRule",
        on_delete=models.PROTECT,
        related_name="feeding_rule_animal_feeding_rule"
    )

    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="feeding_rule_animal_animal"
    )

__all__ = ["TypeFeed", "Feeding", "FeedingRule", "FeedingRuleAnimal"]