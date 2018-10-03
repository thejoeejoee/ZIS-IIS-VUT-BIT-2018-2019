# coding=utf-8
from django.db import models
from .base import BaseModel, BaseTypeModel


class TypePeriodicity(BaseTypeModel):
    name = models.CharField(max_length=128)


class Periodicity(BaseModel):
    type_periodicity = models.ForeignKey(
        "core.TypePeriodicity",
        on_delete=models.PROTECT,
        related_name="periodicity_type_periodicity"
    )

    period = models.PositiveIntegerField()

__all__ = ["TypePeriodicity", "Periodicity"]
