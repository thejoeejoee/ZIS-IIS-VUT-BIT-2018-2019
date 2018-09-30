# coding=utf-8
from django.db import models


class TypeFeed(models.Model):
    name = models.CharField(max_length=128)


class FeedingRule(models.Model):
    feed_type = models.ForeignKey(
        "core.TypeFeed",
        on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()
    periodicity = models.ForeignKey(
        "core.Periodicity",
        on_delete=models.CASCADE)
    feeded_animals = models.ManyToManyField("core.Animal")
    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)


class Feeding(models.Model):
    rule = models.ForeignKey(
        "core.FeedingRule",
        on_delete=models.CASCADE)
    executor = models.ForeignKey(
        "core.AnimalKeeper",
        null=True,
        on_delete=models.SET_NULL)