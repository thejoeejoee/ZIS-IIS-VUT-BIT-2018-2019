# coding=utf-8
from datetime import timedelta
from typing import Tuple, Dict, Callable, Union

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F, DateTimeField, ExpressionWrapper, QuerySet
from django.db.models.constants import LOOKUP_SEP
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _

from .base import BaseModel, BaseTypeModel


class TypeRole(BaseTypeModel):
    pass


class Person(BaseModel):
    type_role = models.ForeignKey(
        "core.TypeRole",
        on_delete=models.PROTECT,
        related_name="person_type_role"
    )

    user = models.OneToOneField(
        get_user_model(),
        related_name='person_user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=256, verbose_name=_("First name"))
    last_name = models.CharField(max_length=256, verbose_name=_("Last name"))

    birth_date = models.DateField(verbose_name=_("Birth date"))
    education = models.TextField(null=True, blank=True, verbose_name=_("Education"))
    note = models.TextField(null=True, blank=True, verbose_name=_("Note"))

    trained_type_animals = models.ManyToManyField(
        "core.TypeAnimal",
        through="core.PersonTypeAnimal",
        help_text=_("Type animals that person is qualified for to feed."),
        blank=True,
        verbose_name=_("Animal types qualification")
    )

    trained_type_enclosures = models.ManyToManyField(
        "core.TypeEnclosure",
        through="core.PersonTypeEnclosure",
        help_text=_("Type enclosures that is qualified to clean."),
        blank=True,
        verbose_name=_("Enclosure types qualification")
    )

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ('type_role__order', 'last_name', 'first_name',)

    def find_in_time(self, start: datetime, length: timedelta) -> Tuple[QuerySet, QuerySet]:
        """
        Finds some activities in given time range - (QS(Feeding), QS(Cleaning)).
        """
        # TODO: I'am not 100 % sure.
        end = start + length

        field_factory = lambda prefix: dict(
            end=ExpressionWrapper(
                F('{}date'.format(prefix + LOOKUP_SEP if prefix else '')) +
                F('{}length'.format(prefix + LOOKUP_SEP if prefix else '')),
                output_field=DateTimeField()
            ),
            start=F('{}date'.format(prefix + LOOKUP_SEP if prefix else ''))
        )  # type: Callable[[str], Dict[str, Union[ExpressionWrapper, F]]]

        q = (
                Q(end__gt=start, end__lt=end) |
                Q(start__gt=start, start__lt=end) |
                Q(start__gt=start, end__lt=end) |
                Q(start__lt=start, end__gt=end) |
                Q(start=start, end=end)
        )

        feeding_conflict = self.feeding_executor.annotate(**field_factory(prefix='')).filter(q)
        cleaning_conflict = self.cleaning_person_person.annotate(**field_factory(prefix='cleaning')).filter(q)

        from ziscz.core.models import Cleaning
        return feeding_conflict, Cleaning.objects.filter(pk__in=cleaning_conflict.values_list('cleaning_id'))


__all__ = ["TypeRole", "Person"]
