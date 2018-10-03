# coding=utf-8
from django.contrib.auth import get_user_model
from django.db import models
from .base import BaseModel, BaseTypeModel


class TypeDegree(BaseTypeModel):
    pass


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

    degree = models.ForeignKey(
        "core.TypeDegree",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="person_degree"
    )

    birth_date = models.DateField()
    education = models.CharField(max_length=512)


__all__ = ["TypeDegree", "TypeRole", "Person"]

