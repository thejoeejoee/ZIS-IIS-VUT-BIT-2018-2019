# coding=utf-8
from __future__ import unicode_literals

import typing

import dateutil.parser as parser
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, ExpressionWrapper, F, DateTimeField, Q
from rest_framework.filters import BaseFilterBackend

if typing.TYPE_CHECKING:
    from rest_framework.views import APIView


class CalendarFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request: WSGIRequest, queryset: QuerySet, view: "APIView"):
        end_field = ExpressionWrapper(F('date') + F('length'), output_field=DateTimeField())

        q = Q()
        if request.GET.get('start'):
            # TODO: respect TZ
            q &= Q(date__gte=parser.parse(request.GET.get('start')))

        if request.GET.get('end'):
            q &= Q(end_x__lt=parser.parse(request.GET.get('end')))

        return queryset.annotate(end_x=end_field).filter(q)
