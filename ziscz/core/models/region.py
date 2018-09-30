# coding=utf-8
from django.db import models


class RegionType(models.Model):
    name = models.CharField(max_length=128)


class Country(models.Model):
    name = models.CharField(max_length=512)