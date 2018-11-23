# coding=utf-8
from __future__ import unicode_literals

import typing

from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from ziscz.core.models import Feeding, Cleaning

if typing.TYPE_CHECKING:
    pass


class DateTimeFieldWihTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class CalendarEventSerializer(ModelSerializer):
    title = CharField(source='specification')
    start = DateTimeFieldWihTZ(source='date')
    end = DateTimeFieldWihTZ()

    class Meta:
        model = Feeding
        fields = (
            'id',
            'title',
            'start',
            'end',
        )


class FeedingCalendarSerializer(CalendarEventSerializer):
    class Meta(CalendarEventSerializer.Meta):
        model = Feeding


class CleaningCalendarSerializer(CalendarEventSerializer):
    class Meta(CalendarEventSerializer.Meta):
        model = Cleaning
