# coding=utf-8
import typing
from typing import Iterable
from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

if typing.TYPE_CHECKING:
    from ziscz.core.models import Person


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    x_created = CreationDateTimeField()
    x_modified = ModificationDateTimeField()

    class Meta:
        abstract = True


class BaseTypeModel(BaseModel):
    identifier = models.CharField(
        verbose_name=_('Identifier'),
        unique=True,
        max_length=128,
        null=True,
        blank=True
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Order'),
    )

    class Meta:
        ordering = "order",
        abstract = True

    def __str__(self):
        return self.name or self.identifier


PERMISSION_CAN_MARK_OWN_EVENT_AS_DONE = 'can_mark_own_event_as_done'


class BaseEventModel(BaseModel):
    date = models.DateTimeField(help_text=_('Planned start of cleaning.'))
    length = models.DurationField()
    done = models.BooleanField(default=False)

    PERMISSION_CAN_MARK_OWN_EVENT_AS_DONE = PERMISSION_CAN_MARK_OWN_EVENT_AS_DONE

    class Meta:
        abstract = True
        ordering = 'date',
        permissions = (
            (PERMISSION_CAN_MARK_OWN_EVENT_AS_DONE, _('Can mark own event as done')),
        )

    @property
    def start_date(self):
        return self.date.date()

    @property
    def end(self):
        return self.date + self.length

    @end.setter
    def end(self, v):
        # dummy setter to allow annotating querysets with end= attribute
        pass

    def get_executors(self) -> Iterable["Person"]:
        raise NotImplementedError
