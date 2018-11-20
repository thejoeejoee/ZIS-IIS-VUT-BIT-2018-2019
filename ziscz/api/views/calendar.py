# coding=utf-8
from __future__ import unicode_literals

from rest_framework.generics import ListAPIView

from ziscz.api.filters import CalendarFilterBackend
from ziscz.api.serializers.calendar import FeedingCalendarSerializer, CleaningCalendarSerializer
from ziscz.core.models import Cleaning, Feeding


class CleaningCalendarView(ListAPIView):
    queryset = Cleaning.objects.all()
    serializer_class = CleaningCalendarSerializer
    filter_backends = (CalendarFilterBackend,)


class FeedingCalendarView(ListAPIView):
    queryset = Feeding.objects.all()
    serializer_class = FeedingCalendarSerializer
    filter_backends = (CalendarFilterBackend,)
