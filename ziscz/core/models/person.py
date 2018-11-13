# coding=utf-8
from datetime import timedelta
from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F, DateTimeField, ExpressionWrapper, QuerySet
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

    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    birth_date = models.DateField()
    education = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    trained_type_animals = models.ManyToManyField(
        "core.TypeAnimal",
        through="core.PersonTypeAnimal",
        help_text=_("Type animals that is qualified to feed."),
        blank=True,
    )

    trained_type_enclosures = models.ManyToManyField(
        "core.TypeEnclosure",
        through="core.PersonTypeEnclosure",
        help_text=_("Type enclosures that is qualified to clean."),
        blank=True,
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
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        feeding_conflict = self.feeding_executor.annotate(
            start=F('date'),
            end=end_field
        ).filter(
            Q(end__gt=start, end__lt=end) |
            Q(start__gt=start, start__lt=end) |
            Q(start__gt=start, end__lt=end) |
            Q(start__lt=start, end__gt=end)
        )

        end_field = ExpressionWrapper(F('cleaning__date') + F('cleaning__length'), output_field=DateTimeField())

        cleaning_conflict = self.cleaning_person_person.annotate(
            start=F('cleaning__date'),
            end=end_field
        ).filter(
            Q(end__gt=start, end__lt=end) |
            Q(start__gt=start, start__lt=end) |
            Q(start__gt=start, end__lt=end) |
            Q(start__lt=start, end__gt=end)
        )

        from ziscz.core.models import Cleaning
        return feeding_conflict, Cleaning.objects.filter(pk__in=cleaning_conflict.values_list('cleaning_id'))


__all__ = ["TypeRole", "Person"]
