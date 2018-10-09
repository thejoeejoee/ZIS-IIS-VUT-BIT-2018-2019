# coding=utf-8
from django.db import models

from .base import BaseModel, BaseTypeModel


class TypeCleaningAccessory(BaseTypeModel):
    """
    Type vybavení pro úklid.
    """
    pass


class TypeEnclosure(BaseTypeModel):
    """
    Typ výběhu se svým požadovaným vybavením.
    """
    required_cleaning_accessory = models.ManyToManyField(
        "core.TypeCleaningAccessory",
        through="core.TypeEnclosureTypeCleaningAccessory"
    )


class Enclosure(BaseModel):
    """
    Výběh.
    """
    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_type_enclosure"
    )

    min_cleaning_duration = models.DurationField()
    min_cleaners_count = models.PositiveIntegerField()

    trained_persons = models.ManyToManyField(
        "core.Person",
        through="core.EnclosurePerson"
    )


class Cleaning(models.Model):
    """
    Pravidlo pro úklid výběhu.
    """
    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.PROTECT,
        related_name="cleaning_enclosure"
    )

    executors = models.ManyToManyField(
        "core.Person",
        through="core.CleaningPerson"
    )

    date = models.DateTimeField()

    length = models.DurationField()

    done = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)


class EnclosurePerson(BaseModel):
    """
    Člověk vyškolený k čištění výběhu.
    """
    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_person_enclosure"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="enclosure_person_person"
    )


class TypeEnclosureTypeCleaningAccessory(BaseModel):
    """
    Spojení výběhu s požadovaným vybavením k čištění.
    """
    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="type_enclosure_type_cleaning_accessory_type_enclosure"
    )

    type_cleaning_accessory = models.ForeignKey(
        "core.TypeCleaningAccessory",
        on_delete=models.PROTECT,
        related_name="type_enclosure_type_cleaning_accessory_type_cleaning_accessory"
    )


class CleaningPerson(BaseModel):
    cleaning = models.ForeignKey(
        "core.Cleaning",
        on_delete=models.PROTECT,
        related_name="cleaning_person_cleaning"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="cleaning_person_person"
    )


__all__ = ["TypeCleaningAccessory", "TypeEnclosure", "Enclosure", "EnclosurePerson",
           "TypeEnclosureTypeCleaningAccessory"]
