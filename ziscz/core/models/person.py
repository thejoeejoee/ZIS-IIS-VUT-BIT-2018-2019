# coding=utf-8
from django.db import models


class TypeDegree(models.Model):
    name = models.CharField(max_length=256)


class PersonRole(models.Model):
    name = models.CharField(max_length=128)


class Person(models.Model):
    role = models.ForeignKey("core.PersonRole", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    degree = models.ForeignKey(
        "core.TypeDegree",
        null=True,
        on_delete=models.SET_NULL)
    birth_date = models.DateField()
    education = models.CharField(max_length=512)


class AnimalKeeper(Person):
    trained_for_animals = models.ManyToManyField("core.Animal")
    trained_for_enclosures_cleaning = models.ManyToManyField("core.Enclosure")