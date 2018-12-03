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


class BaseCalendarEventSerializer(ModelSerializer):
    title = CharField(source='specification')
    start = DateTimeFieldWihTZ(source='date')
    end = DateTimeFieldWihTZ()

    class Meta:
        fields = (
            'id',
            'title',
            'start',
            'end',
            'done',
            'color',
            'its_too_late_to_apologize',
            'description',
        )


class FeedingCalendarSerializer(BaseCalendarEventSerializer):
    class Meta(BaseCalendarEventSerializer.Meta):
        model = Feeding


class CleaningCalendarSerializer(BaseCalendarEventSerializer):
    class Meta(BaseCalendarEventSerializer.Meta):
        model = Cleaning
