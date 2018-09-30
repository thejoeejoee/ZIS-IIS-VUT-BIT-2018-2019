# coding=utf-8
from django.db import models


class PeriodicityType(models.Model):
    name = models.CharField(max_length=128)


class Periodicity(models.Model):
    type = models.ForeignKey(
        "core.PeriodicityType",
        on_delete=models.CASCADE)
    period = models.PositiveIntegerField()
