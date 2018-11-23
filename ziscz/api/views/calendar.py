# coding=utf-8
from __future__ import unicode_literals

from typing import Union, Type

import pytz
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from dateutil import parser
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ExpressionWrapper, Case, When, Value, BooleanField
from django.db.models.functions import Now
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import View
from rest_framework.fields import NullBooleanField
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer

from ziscz.api.filters import CalendarFilterBackend
from ziscz.api.serializers.calendar import FeedingCalendarSerializer, CleaningCalendarSerializer
from ziscz.core.models import Cleaning, Feeding
from ziscz.core.models.base import BaseEventModel


def _to_representation_with_editable_remove(serializer: Type[ModelSerializer]):
    def _(self: ModelSerializer, obj: BaseEventModel):
        data = super(serializer, self).to_representation(obj)
        if data.get('editable') is None:
            del data['editable']
        return data

    return _


def _calendar_event_view_factory(model: Type[BaseEventModel], serializer: Type[ModelSerializer]) -> type:
    return type(
        'view',
        (ListAPIView,),
        dict(
            queryset=model.objects.annotate(
                editable=ExpressionWrapper(
                    # TODO: check TZ
                    Case(
                        When(
                            date__gte=Now(),
                            then=Value(None)
                        ),
                        default=Value(False),
                        output_field=BooleanField(),
                    ),
                    output_field=BooleanField(),
                )
            ),
            filter_backends=(CalendarFilterBackend,),
            serializer_class=type(
                'serializer',
                (serializer,),
                dict(
                    editable=NullBooleanField(),
                    to_representation=_to_representation_with_editable_remove(serializer=serializer),
                    Meta=type(
                        'meta',
                        (serializer.Meta,),
                        dict(
                            fields=serializer.Meta.fields + ('editable',),
                        )
                    )
                )
            )
        )
    )


CleaningCalendarView = _calendar_event_view_factory(
    model=Cleaning,
    serializer=CleaningCalendarSerializer
)

FeedingCalendarView = _calendar_event_view_factory(
    model=Feeding,
    serializer=FeedingCalendarSerializer
)


def find_event(pk) -> Union[Cleaning, Feeding]:
    try:
        return get_object_or_404(Feeding, pk=pk)
    except Http404:
        return get_object_or_404(Cleaning, pk=pk)


# TODO: cannot move to history
# TODO: cannot move already done event
class CalendarEventStartChangeView(CsrfExemptMixin, JsonRequestResponseMixin, PermissionRequiredMixin, View):
    require_json = True
    permission_required = 'core.change_cleaning', 'core.change_feeding'

    def post(self, request: WSGIRequest, *args, **kwargs):
        data = self.request_json

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
class CalendarEventEndChangeView(CsrfExemptMixin, JsonRequestResponseMixin, PermissionRequiredMixin, View):
    require_json = True
    permission_required = 'core.change_cleaning', 'core.change_feeding'

    def post(self, request: WSGIRequest, *args, **kwargs):
        data = self.request_json

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
