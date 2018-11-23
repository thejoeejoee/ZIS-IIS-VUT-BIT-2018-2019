# coding=utf-8
from __future__ import unicode_literals

from typing import Union

import pytz
from dateutil import parser
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.utils import json

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


def find_event(pk) -> Union[Cleaning, Feeding]:
    try:
        return get_object_or_404(Feeding, pk=pk)
    except Http404:
        return get_object_or_404(Cleaning, pk=pk)


@method_decorator(csrf_exempt, name='dispatch')
class CalendarEventStartChangeView(View):
    def post(self, request: WSGIRequest, *args, **kwargs):
        data = json.loads(request.body.decode())

        event = find_event(data.get('id'))
        start = parser.parse(data.get('start')).astimezone(pytz.utc)

        if isinstance(event, Cleaning):
            for executor in event.executors.all():
                conflict_feeding, conflict_cleaning = executor.find_in_time(
                    start=start,
                    length=event.length,
                )
                if conflict_feeding.exclude(pk=event.pk).exists() or conflict_cleaning.exclude(pk=event.pk).exists():
                    return JsonResponse(dict(
                        success=False,
                        message=_('Reverted, conflict in time plan of executor {}.').format(executor)
                    ))
            event.date = start
            event.save(update_fields=['date'])

        elif isinstance(event, Feeding):
            conflict_feeding, conflict_cleaning = event.executor.find_in_time(
                start=start,
                length=event.length,
            )
            if conflict_feeding.exclude(pk=event.pk).exists() or conflict_cleaning.exclude(pk=event.pk).exists():
                return JsonResponse(dict(
                    success=False,
                    message=_('Reverted, conflict in time plan of executor {}.').format(event.executor)
                ))
            event.date = start
            event.save(update_fields=['date'])

        else:
            return JsonResponse(dict(success=False, message=_('Unknown action to move.')))
        return JsonResponse(dict(success=True, message=_('Event successfully moved.')))


# TODO: "little" bit copypasted...
@method_decorator(csrf_exempt, name='dispatch')
class CalendarEventEndChangeView(View):
    def post(self, request: WSGIRequest, *args, **kwargs):
        data = json.loads(request.body.decode())

        event = find_event(data.get('id'))
        end = parser.parse(data.get('end')).astimezone(pytz.utc)
        length = end - event.date

        if isinstance(event, Cleaning):
            for executor in event.executors.all():
                conflict_feeding, conflict_cleaning = executor.find_in_time(
                    start=event.date,
                    length=length,
                )
                if conflict_feeding.exclude(pk=event.pk).exists() or conflict_cleaning.exclude(pk=event.pk).exists():
                    return JsonResponse(dict(
                        success=False,
                        message=_('Reverted, conflict in time plan of executor {}.').format(executor)
                    ))
            if length < event.enclosure.min_cleaning_duration:
                return JsonResponse(dict(
                    success=False,
                    message=_('Reverted, {} is the minimal duration of cleaning {}.').format(
                        event.enclosure.min_cleaning_duration,
                        event.enclosure
                    )
                ))

            event.length = length
            event.save(update_fields=['length'])

        elif isinstance(event, Feeding):
            conflict_feeding, conflict_cleaning = event.executor.find_in_time(
                start=event.date,
                length=length,
            )
            if conflict_feeding.exclude(pk=event.pk).exists() or conflict_cleaning.exclude(pk=event.pk).exists():
                return JsonResponse(dict(
                    success=False,
                    message=_('Reverted, conflict in time plan of executor {}.').format(event.executor)
                ))
            event.length = length
            event.save(update_fields=['length'])

        else:
            return JsonResponse(dict(success=False, message=_('Unknown action to move.')))
        return JsonResponse(dict(success=True, message=_('Length of event successfully changed.')))
