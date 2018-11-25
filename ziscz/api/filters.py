# coding=utf-8
from __future__ import unicode_literals

import typing

import dateutil.parser as parser
import pytz
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, ExpressionWrapper, F, DateTimeField, Q
from django.utils.timezone import get_current_timezone
from pytz import UnknownTimeZoneError
from rest_framework.filters import BaseFilterBackend

if typing.TYPE_CHECKING:
    from rest_framework.views import APIView


class CalendarFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request: WSGIRequest, queryset: QuerySet, view: "APIView"):
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())

        try:
            tz = pytz.timezone(request.GET.get('timezone'))
        except UnknownTimeZoneError:
            tz = get_current_timezone()

        q = Q()
        if request.GET.get('start'):
            q &= Q(date__gte=parser.parse(request.GET.get('start')).replace(tzinfo=tz))

        if request.GET.get('end'):
            q &= Q(end__lt=parser.parse(request.GET.get('end')).replace(tzinfo=tz))

        return queryset.annotate(end=end_field).filter(q)
