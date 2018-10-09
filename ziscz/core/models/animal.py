# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _

from .base import BaseModel, BaseTypeModel


class TypeAnimal(BaseTypeModel):
    pass


class Animal(BaseModel):
    """
    Zvíře jako takové.
    """
    name = models.CharField(verbose_name=_('Name'), max_length=64)

    type_animal = models.ForeignKey(
        "core.TypeAnimal",
        on_delete=models.PROTECT,
        related_name="animal_type_animal"
    )

    birth_date = models.DateField(null=True, blank=True)

    origin_country = models.ForeignKey(
        "core.TypeCountry",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_origin_country"
    )

    occurence_region = models.ManyToManyField(
        "core.TypeRegion",
        through="core.AnimalRegion"
    )

    parent1 = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_parent1"
    )

    parent2 = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_parent2"
    )

    death_date = models.DateTimeField(blank=True, null=True)

    trained_person = models.ManyToManyField(
        "core.Person",
        through="core.AnimalPerson"
    )

    class Meta:
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self):
        return ' '.join(map(str, (self.type_animal, self.name)))


class AnimalStay(BaseModel):
    """
    Umístění zvířete do výběhu, od do.
    """
    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="animal_stays"
    )

    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.PROTECT,
        related_name="animal_stays"
    )

    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)


class AnimalPerson(BaseModel):
    """
    Vyškolení osoby pro krmení zvířete.
    """
    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="animal_person_animal"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="animal_person_person"
    )

    class Meta:
        unique_together = (
            ('animal', 'person'),
        )


class AnimalRegion(BaseModel):
    """
    Oblasti výskytu zvířete.
    """
    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="animal_region_animal"
    )

    region = models.ForeignKey(
        "core.TypeRegion",
        on_delete=models.PROTECT,
        related_name="animal_region_region"
    )


__all__ = ["Animal", "AnimalStay", "AnimalRegion", "TypeAnimal", "AnimalPerson"]
