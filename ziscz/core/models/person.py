# coding=utf-8

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

from .base import BaseModel, BaseTypeModel


class TypeRole(BaseTypeModel):
    pass


class Person(BaseModel):
    type_role = models.ForeignKey(
        "core.TypeRole",
        on_delete=models.PROTECT,
        related_name="person_type_role"
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    birth_date = models.DateField()
    education = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ('last_name', 'first_name',)


__all__ = ["TypeRole", "Person"]
