# coding=utf-8
from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    x_created = CreationDateTimeField()
    x_updated = ModificationDateTimeField()

    class Meta:
        abstract = True


class BaseTypeModel(BaseModel):
    identifier = models.CharField(
        verbose_name=_('Identifier'),
        unique=True,
        max_length=128,
        null=True,
        blank=True
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Order'),
    )

    class Meta:
        ordering = "order",
        abstract = True

    def __str__(self):
        return self.name or self.identifier