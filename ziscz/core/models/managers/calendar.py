# coding=utf-8
from __future__ import unicode_literals

import typing

from django.db.models import Manager, QuerySet, ExpressionWrapper, F, DateTimeField
from django.db.transaction import atomic
from django.utils import timezone

if typing.TYPE_CHECKING:
    pass


class CurrentEventManagerMixin(object):
    @atomic
    def current(self) -> QuerySet:
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())
        now = timezone.now()
        return self.get_queryset().annotate(end_x=end_field).filter(
            date__lte=now,
            end_x__gte=now
        )


class CleaningManager(CurrentEventManagerMixin, Manager):
    pass


class FeedingManager(CurrentEventManagerMixin, Manager):
    pass
