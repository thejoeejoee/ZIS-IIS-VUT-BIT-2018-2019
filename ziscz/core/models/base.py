# coding=utf-8
from uuid import uuid4
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    x_created = CreationDateTimeField()
    x_updated = ModificationDateTimeField()

    class Meta:
        abstract = True


class BaseTypeModel(BaseModel):
    identifier = models.CharField(unique=True, max_length=128, null=True, blank=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = "order",
        abstract = True
