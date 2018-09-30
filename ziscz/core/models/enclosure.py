# coding=utf-8
from django.db import models


class CleaningAccessory(models.Model):
    name = models.CharField(max_length=128)


class EnclosureType(models.Model):
    name = models.CharField(max_length=128)


class Enclosure(models.Model):
    type = models.ForeignKey(
        "core.EnclosureType",
        on_delete=models.CASCADE)
    min_cleaning_duration = models.DurationField()
    min_cleaners_count = models.PositiveIntegerField()
    required_cleaning_accessory = models.ManyToManyField("core.CleaningAccessory")


class EnclosureCleaningRule(models.Model):
    enclosure_type = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.CASCADE)
    periodicity = models.ForeignKey(
        "core.Periodicity",
        on_delete=models.CASCADE)
    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)


class EnclosureCleaning(models.Model):
    rule = models.ForeignKey(
        "core.EnclosureCleaning",
        on_delete=models.CASCADE)
    executors = models.ManyToManyField("core.AnimalKeeper")
