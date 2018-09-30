# coding=utf-8
from django.db import models


class AnimalType(models.Model):
    name = models.CharField(max_length=256)


class Animal(models.Model):
    type = models.ForeignKey(
        "core.AnimalType",
        on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    country_of_origin = models.ForeignKey(
        "core.Country",
        null=True,
        on_delete=models.SET_NULL)
    region_of_occurence = models.ForeignKey(
        "core.RegionType",
        null=True,
        on_delete=models.SET_NULL)
    parent1 = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL)
    parent2 = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL)
    death_date = models.DateTimeField()


class AnimalStay(models.Model):
    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.CASCADE)
    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.CASCADE)
    from_ = models.DateField()
    to = models.DateField()