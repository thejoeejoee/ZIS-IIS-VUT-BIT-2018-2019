# coding=utf-8
from __future__ import unicode_literals

import typing
from datetime import timedelta
from typing import Optional

from django.db.models import Manager, Q
from django.db.transaction import atomic
from django.utils import timezone

if typing.TYPE_CHECKING:
    from ziscz.core.models import Animal, Enclosure, AnimalStay


class AnimalStayManager(Manager):
    @atomic
    def move_animal(self, animal: "Animal", new_enclosure: Optional["Enclosure"]) -> Optional["AnimalStay"]:
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        self.filter(
            self.model.filter_for_actual(),
            animal=animal,
        ).update(date_to=yesterday)

        if not new_enclosure:
            return

        return self.create(
            animal=animal,
            enclosure=new_enclosure,
            date_from=today,
            date_to=None,
        )


class LiveAnimalsManager(Manager):
    @staticmethod
    def get_dead_filter() -> Q:
        today = timezone.now().date()
        return Q(
            death_date__isnull=False,
            death_date__lte=today,
        )

    def get_queryset(self):
        return super().get_queryset().filter(~self.get_dead_filter())
