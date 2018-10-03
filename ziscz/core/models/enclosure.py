# coding=utf-8
from django.db import models
from .base import BaseModel, BaseTypeModel


class TypeCleaningAccessory(BaseTypeModel):
    pass

class TypeEnclosure(BaseTypeModel):
    required_cleaning_accessory = models.ManyToManyField(
        "core.TypeCleaningAccessory",
        through="core.TypeEnclosureTypeCleaningAccessory"
    )


class Enclosure(BaseModel):
    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_type_enclosure"
    )

    min_cleaning_duration = models.DurationField()
    min_cleaners_count = models.PositiveIntegerField()

    trained_person = models.ManyToManyField(
        "core.Person",
        through="core.EnclosurePerson"
    )


class EnclosureCleaningRule(models.Model):
    enclosure_type = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_cleaning_rule_enclosure_type"
    )

    periodicity = models.ForeignKey(
        "core.Periodicity",
        on_delete=models.PROTECT,
        related_name="enclosure_cleaning_rule_periodicity"
    )

    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)


class EnclosureCleaning(BaseModel):
    rule = models.ForeignKey(
        "core.EnclosureCleaning",
        on_delete=models.PROTECT,
        related_name="enclosure_cleaning_rule"
    )

    executors = models.ManyToManyField(
        "core.Person",
        through="core.EnclosureCleaningPerson"
    )


class EnclosurePerson(BaseModel):
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

class EnclosureCleaningPerson(BaseModel):
    enclosure_cleaning = models.ForeignKey(
        "core.EnclosureCleaning",
        on_delete=models.PROTECT,
        related_name="enclosure_cleaning_person_enclosure_cleaning"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="enclosure_cleaning_person_person"
    )

__all__ = ["TypeCleaningAccessory", "TypeEnclosure", "Enclosure", "EnclosureCleaning",
           "EnclosureCleaningRule", "EnclosurePerson",
           "TypeEnclosureTypeCleaningAccessory", "EnclosureCleaningPerson"]
