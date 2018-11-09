# coding=utf-8
import typing

from colorful.fields import RGBColorField
from django.db import models
from django.utils import timezone
from django.utils.formats import time_format
from django.utils.translation import ugettext as _

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

    color = RGBColorField(
        null=True, blank=True,
        help_text=_('Describing color used for type of enclosure in system UI as helper, black is default.')
    )

    trained_persons = models.ManyToManyField(
        "core.Person",
        through="core.PersonTypeEnclosure"
    )


class Enclosure(BaseModel):
    """
    Výběh.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=64)

    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_type_enclosure"
    )

    color = RGBColorField(
        null=True, blank=True,
        help_text=_('Describing color used in system UI as helper, black is default.')
    )

    min_cleaning_duration = models.DurationField()
    min_cleaners_count = models.PositiveIntegerField()

    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Enclosure')
        verbose_name_plural = _('Enclosures')
        ordering = ('type_enclosure__order', 'name',)

    def __str__(self):
        return self.name

    @property
    def enclosure_color(self):
        # black is default for rgb fields
        return (self.color if self.color != '#000000' else None) or self.type_enclosure.color

    @property
    def current_animals(self):
        from ziscz.core.models import Animal, AnimalStay
        return Animal.live_animals.filter(
            AnimalStay.filter_for_actual('animal_stay_animal'),
            animal_stay_animal__enclosure=self,
        ).select_related(
            'type_animal',
        )

    @property
    def last_cleaning(self) -> typing.Optional["Cleaning"]:
        today = timezone.now().date()
        return self.cleaning_enclosure.filter(
            done=True,
            date__lt=today
        ).order_by('date').last()


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

    date = models.DateTimeField(help_text=_('Planned start of cleaning.'))

    length = models.DurationField()

    done = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)

    @property
    def specification(self):
        return _('Cleaning for {} at {} ({}).').format(
            self.enclosure,
            time_format(self.date),
            ', '.join(map(str, self.executors.all())),
        )

    @property
    def start_date(self):
        return self.date.date()


class PersonTypeEnclosure(BaseModel):
    """
    Člověk vyškolený k čištění typu výběhu.
    """
    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="person_type_enclosure_type_enclosure"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.PROTECT,
        related_name="person_type_enclosure_person"
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


__all__ = ["TypeCleaningAccessory", "TypeEnclosure", "Enclosure", "PersonTypeEnclosure",
           "TypeEnclosureTypeCleaningAccessory", "CleaningPerson", "Cleaning"]
