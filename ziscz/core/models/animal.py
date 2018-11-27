# coding=utf-8
from django.conf import settings
from django.db import models
from django.db.models import Q, Manager, QuerySet
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from relativefilepathfield.fields import RelativeFilePathField

from ziscz.core.models.managers.animal import AnimalStayManager, LiveAnimalsManager
from .base import BaseModel, BaseTypeModel


class TypeAnimal(BaseTypeModel):
    icon = RelativeFilePathField(
        path=settings.ICONS_PATH,
        blank=True,
        null=True
    )

    trained_persons = models.ManyToManyField(
        "core.Person",
        through="core.PersonTypeAnimal"
    )

    class Meta(BaseTypeModel.Meta):
        verbose_name = _("Type animal")
        verbose_name_plural = _("Types animal")


class Animal(BaseModel):
    """
    Zvíře jako takové.
    """
    objects = Manager()
    live_animals = LiveAnimalsManager()

    name = models.CharField(verbose_name=_('Name'), max_length=64)

    type_animal = models.ForeignKey(
        "core.TypeAnimal",
        on_delete=models.PROTECT,
        related_name="animal_type_animal",
        verbose_name=_("Type")
    )

    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth date'))

    origin_country = models.ForeignKey(
        "core.TypeCountry",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_origin_country",
        verbose_name=_("Origin country")
    )

    occurrence_region = models.ManyToManyField(
        "core.TypeRegion",
        through="core.AnimalRegion",
        verbose_name=_('Occurrence regions')
    )

    parent1 = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_parent1",
        verbose_name=_("Parent")
    )

    parent2 = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="animal_parent2",
        verbose_name=_("Parent")
    )

    death_date = models.DateField(blank=True, null=True, verbose_name=_("Death date"))

    class Meta:
        ordering = '-death_date', 'type_animal', 'name',
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self):
        return ' '.join(map(str, (self.type_animal, self.name)))

    @cached_property
    def actual_enclosure(self):
        try:
            # prefetched
            return self.animal_stay_animal_actual[0].enclosure
        except (AttributeError, IndexError):
            stay = self.animal_stay_animal.filter(AnimalStay.filter_for_actual()).first()
            return stay.enclosure if stay else None

    @cached_property
    def children(self):
        return self.animal_parent1.all() | self.animal_parent2.all()

    @cached_property
    def dead(self) -> bool:
        today = timezone.now().date()
        return self.death_date and self.death_date <= today

    @cached_property
    def planned_feedings(self) -> QuerySet:
        # could be prefetched
        today = timezone.localdate()
        return self.feeding_animal_animal.filter(
            feeding__date__gte=today
        ).order_by('-feeding__date')


class AnimalStay(BaseModel):
    """
    Umístění zvířete do výběhu, od do.
    """

    objects = AnimalStayManager()

    animal = models.ForeignKey(
        "core.Animal",
        on_delete=models.PROTECT,
        related_name="animal_stay_animal"
    )

    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.PROTECT,
        related_name="animal_stay_enclosure"
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

    class Meta:
        ordering = 'date_from',
        verbose_name = _("Animal stay")
        verbose_name_plural = _("Animal stays")


class PersonTypeAnimal(BaseModel):
    """
    Vyškolení osoby pro krmení typ zvířete.
    """
    type_animal = models.ForeignKey(
        "core.TypeAnimal",
        on_delete=models.PROTECT,
        related_name="person_type_animal_type_animal"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="person_type_animal_person"
    )

    class Meta:
        unique_together = (
            ('type_animal', 'person'),
        )
        verbose_name = _("Person trained on animal")


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

    class Meta:
        verbose_name = _("Animal region")
        verbose_name_plural = _("Animal regions")


__all__ = ["Animal", "AnimalStay", "AnimalRegion", "TypeAnimal", "PersonTypeAnimal"]
