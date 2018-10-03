# coding=utf-8
from django.db import models
from .base import BaseModel, BaseTypeModel


class TypeDegree(BaseTypeModel):
    pass


class PersonRole(BaseModel):
    name = models.CharField(max_length=128)


class Person(BaseModel):
    role = models.ForeignKey(
        "core.PersonRole",
        on_delete=models.PROTECT,
        related_name="person_role"
    )

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    degree = models.ForeignKey(
        "core.TypeDegree",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="person_degree"
    )

    birth_date = models.DateField()
    education = models.CharField(max_length=512)

__all__ = ["TypeDegree", "PersonRole", "Person"]
