# coding=utf-8
import typing
from typing import Iterable

from colorful.fields import RGBColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.formats import time_format, date_format
from django.utils.timezone import localtime, localdate
from django.utils.translation import ugettext_lazy as _, ungettext

from .base import BaseModel, BaseTypeModel
from ..models.base import BaseEventModel
from ..models.managers.calendar import CleaningQuerySet

if typing.TYPE_CHECKING:
    pass


class TypeCleaningAccessory(BaseTypeModel):
    """
    Type vybavení pro úklid.
    """

    class Meta(BaseTypeModel.Meta):
        verbose_name = _("Type cleaning accessory")
        verbose_name_plural = _("Types cleaning accessories")


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

    class Meta(BaseTypeModel.Meta):
        verbose_name = _("Type enclosure")
        verbose_name_plural = _("Types enclosures")


class Enclosure(BaseModel):
    """
    Výběh.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=64)

    type_enclosure = models.ForeignKey(
        "core.TypeEnclosure",
        on_delete=models.PROTECT,
        related_name="enclosure_type_enclosure",
        verbose_name=_("Type")
    )

    color = RGBColorField(
        null=True, blank=True,
        help_text=_('Describing color used in system UI as helper, black is default.'),
        verbose_name=_("Color")
    )

    min_cleaning_duration = models.DurationField(
        verbose_name=_("Minimum cleaning duration")
    )
    min_cleaners_count = models.PositiveIntegerField(
        verbose_name=_("Minimum cleaners count"),
        validators=[MinValueValidator(1)]
    )

    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))

    class Meta:
        verbose_name = _('Enclosure')
        verbose_name_plural = _('Enclosures')
        ordering = ('type_enclosure__order', 'name',)

    def __str__(self):
        return self.name

    @property
    def enclosure_color(self) -> str:
        # black is default for rgb fields
        return (self.color if self.color != '#000000' else None) or self.type_enclosure.color

    @property
    def current_animals(self) -> QuerySet:
        from ziscz.core.models import Animal, AnimalStay
        return Animal.live_animals.filter(
            AnimalStay.filter_for_actual('animal_stay_animal'),
            animal_stay_animal__enclosure=self,
        ).select_related(
            'type_animal',
        )

    @property
    def last_cleaning(self) -> typing.Optional["Cleaning"]:
        return self.last_done_cleanings.last()

    @property
    def last_done_cleanings(self) -> QuerySet:
        today = timezone.localdate()
        return self.cleaning_enclosure.filter(
            done=True,
            date__lt=today
        ).order_by('date')

    @property
    def planned_cleanings(self) -> QuerySet:
        today = timezone.localdate()
        return self.cleaning_enclosure.filter(
            date__gte=today
        ).order_by('-date')


class Cleaning(BaseEventModel):
    """
    Pravidlo pro úklid výběhu.
    """

    objects = CleaningQuerySet.as_manager()

    enclosure = models.ForeignKey(
        "core.Enclosure",
        on_delete=models.CASCADE,
        related_name="cleaning_enclosure",
        verbose_name=_('Enclosure'),
    )

    executors = models.ManyToManyField(
        "core.Person",
        through="core.CleaningPerson",
        verbose_name=_('Executors'),
    )

    note = models.TextField(null=True, blank=True, verbose_name=_('Note'), )

    class Meta(BaseEventModel.Meta):
        verbose_name = _('Cleaning')
        verbose_name_plural = _('Cleanings')

    def __str__(self):
        return _('Cleaning at {} {}').format(
            time_format(localtime(self.date)),
            date_format(localdate(self.date)),
        )

    @property
    def specification(self):
        return _('{} by {}').format(
            self.enclosure,
            ', '.join(map(str, self.get_executors())),
        )

    @property
    def description(self):
        needed = self.needed_type_cleaning_accessory
        if needed:
            return ungettext(
                'Needed cleaning accessory: {}',
                'Needed cleaning accessories: {}',
                len(needed),
            ).format(', '.join(map(str, needed)))
        return ''

    def get_executors(self) -> Iterable["CleaningPerson"]:
        return self.executors.all()

    @property
    def needed_type_cleaning_accessory(self):
        # prefetch
        if hasattr(self, '_needed_type_cleaning_accessory'):
            return self._needed_type_cleaning_accessory
        return list(self.enclosure.type_enclosure.required_cleaning_accessory.all())

    @property
    def color(self):
        return '#107180' if self.done else '#17a2b8'


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

    class Meta:
        verbose_name = _("Person types animal")
        verbose_name_plural = _("Person types animal")


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

    class Meta:
        verbose_name = _("Type enclosure type cleaning accessory")
        verbose_name_plural = _("Types enclosure type cleaning accessories")

    def __str__(self):
        return str(self.type_cleaning_accessory)


class CleaningPerson(BaseModel):
    cleaning = models.ForeignKey(
        "core.Cleaning",
        on_delete=models.CASCADE,
        related_name="cleaning_person_cleaning"
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="cleaning_person_person"
    )

    class Meta:
        verbose_name = _("Cleaning person")
        verbose_name_plural = _("Cleaning persons")

    def __str__(self):
        return str(self.person)


__all__ = ["TypeCleaningAccessory", "TypeEnclosure", "Enclosure", "PersonTypeEnclosure",
           "TypeEnclosureTypeCleaningAccessory", "CleaningPerson", "Cleaning"]
