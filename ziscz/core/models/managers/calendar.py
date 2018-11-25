# coding=utf-8
from __future__ import unicode_literals

import typing

from django.db import models
from django.db.models import QuerySet, ExpressionWrapper, F, DateTimeField
from django.utils import timezone

if typing.TYPE_CHECKING:
    from ziscz.core.models import Person


class BaseEventQuerySet(models.QuerySet):
    def filter_by_person(self, person: "Person") -> QuerySet:
        raise NotImplementedError

    def current(self) -> QuerySet:
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        now = timezone.now()
        return self.annotate(end=end_field).filter(
            date__lte=now,
            end__gte=now
        )

    def in_date(self, date=None) -> QuerySet:
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        date = date or timezone.now().date()
        return self.annotate(end=end_field).filter(end__date=date)


class CleaningQuerySet(BaseEventQuerySet):
    def filter_by_person(self, person: "Person") -> QuerySet:
        pass


class FeedingQuerySet(BaseEventQuerySet):
    def filter_by_person(self, person: "Person") -> QuerySet:
        pass
