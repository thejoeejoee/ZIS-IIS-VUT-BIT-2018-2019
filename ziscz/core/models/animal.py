# coding=utf-8
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from ziscz.core.models.managers.animal import AnimalStayManager
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

    occurrence_region = models.ManyToManyField(
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
        ordering = 'name',
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self):
        return ' '.join(map(str, (self.type_animal, self.name)))

    @property
    def actual_enclosure(self):
        stays = self.animal_stays.filter(AnimalStay.filter_for_actual())
        return stays.first().enclosure if stays.exists() else None


class AnimalStay(BaseModel):
    """
    Umístění zvířete do výběhu, od do.
    """

    objects = AnimalStayManager()

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

    @staticmethod
    def filter_for_actual(prefix=None):
        today = timezone.now().date()
        p = lambda i: '{}{}'.format(
            '{}__'.format(prefix) if prefix else '',
            i
        )
        return (
                Q(**{p('date_from__lte'): today}) & (
                Q(**{p('date_to__isnull'): True}) | Q(**{p('date_to__gte'): today}))
        )


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
