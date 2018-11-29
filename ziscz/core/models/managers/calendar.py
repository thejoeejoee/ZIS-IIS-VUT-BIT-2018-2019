# coding=utf-8
from __future__ import unicode_literals

import typing
from datetime import time

from django.db import models
from django.db.models import QuerySet, ExpressionWrapper, F, DateTimeField, Q
from django.utils import timezone

if typing.TYPE_CHECKING:
    from ziscz.core.models import Person


class BaseEventQuerySet(models.QuerySet):
    def filter_by_person(self, person: "Person") -> "BaseEventQuerySet":
        return self.filter(self.person_q(person=person))

    def person_q(self, person: "Person") -> Q:
        raise NotImplementedError

    def current(self) -> "BaseEventQuerySet":
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        now = timezone.localtime()
        return self.annotate(end=end_field).filter(
            date__lte=now,
            end__gte=now
        )

    def in_date(self, date=None) -> "BaseEventQuerySet":
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        date = date or timezone.localdate()
        return self.annotate(end=end_field).filter(
            Q(date__date=date) |  # starts today
            (Q(end__date=date) & ~Q(end__time=time())) # ends today, but not at 00:00
        )


class CleaningQuerySet(BaseEventQuerySet):
    def person_q(self, person: "Person") -> Q:
        return Q(cleaning_person_cleaning__person=person)


class FeedingQuerySet(BaseEventQuerySet):
    def person_q(self, person: "Person") -> Q:
        return Q(executor=person)
