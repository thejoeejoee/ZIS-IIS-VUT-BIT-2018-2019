# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime, timedelta, timezone
from typing import Type, Iterable, Tuple, Callable

import pytz
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from dateutil import parser
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ExpressionWrapper, Case, When, Value, BooleanField, QuerySet, Prefetch
from django.db.models.functions import Now
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import View
from rest_framework.fields import NullBooleanField
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.serializers import ModelSerializer

from ziscz.api.filters import CalendarFilterBackend
from ziscz.api.serializers.calendar import FeedingCalendarSerializer, CleaningCalendarSerializer
from ziscz.core.models import Cleaning, Feeding, Person
from ziscz.core.models.base import BaseEventModel


def _calendar_event_view_factory(model: Type[BaseEventModel], serializer: Type[ModelSerializer],
                                 qs_modifier: Callable[[QuerySet], QuerySet] = lambda qs: qs) -> type:
    class View(ListAPIView):
        class serializer_class(serializer):
            editable = NullBooleanField()
            Meta = type(
                'meta',
                (serializer.Meta,),
                dict(
                    fields=serializer.Meta.fields + ('editable',),
                )
            )

            def to_representation(self: ModelSerializer, obj: BaseEventModel):
                data = super().to_representation(obj)
                if data.get('editable') is None:
                    del data['editable']
                if self.context.get('has_change_perm'):
                    data['url'] = obj.get_absolute_url()
                return data

        queryset = qs_modifier(model.objects.annotate(
            editable=ExpressionWrapper(
                Case(
                    When(
                        date__gte=Now(),
                        then=Value(None)
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
                output_field=BooleanField(),
            ),
        ))
        filter_backends = (CalendarFilterBackend,)

        def get_serializer_context(self):
            ctx = super().get_serializer_context()

            ctx['has_change_perm'] = self.request.user.has_perms(('core.change_cleaning', 'core.change_feeding'))
            return ctx

    return View


def _prefetch_cleaning_accessory(qs: QuerySet):
    return qs.select_related(
        'enclosure',
        'enclosure__type_enclosure',
    ).prefetch_related(
        # TODO: not works properly :-(
        Prefetch(
            'cleaning_person_cleaning__person',
            queryset=Person.objects.get_queryset().select_related('type_role').order_by(*Person._meta.ordering),
            to_attr='_executors',
        ),
        # 'enclosure__type_enclosure__type_enclosure_type_cleaning_accessory_type_enclosure',
        Prefetch(
            'enclosure__type_enclosure__type_enclosure_type_cleaning_accessory_type_enclosure__type_cleaning_accessory',
            to_attr='_needed_type_cleaning_accessory',
        )
    )


CleaningCalendarView = _calendar_event_view_factory(
    model=Cleaning,
    serializer=CleaningCalendarSerializer,
    qs_modifier=_prefetch_cleaning_accessory
)

FeedingCalendarView = _calendar_event_view_factory(
    model=Feeding,
    serializer=FeedingCalendarSerializer
)


class BaseCalendarEventChangeView(CsrfExemptMixin, JsonRequestResponseMixin, PermissionRequiredMixin, View):
    require_json = True
    permission_required = 'core.change_cleaning', 'core.change_feeding'
    models = [Cleaning, Feeding]  # type: Iterable[Type[BaseEventModel]]
    object = None  # type: BaseEventModel

    def post(self, request: WSGIRequest, *args, **kwargs):
        self.object = self.get_object()

        start, length = self.get_interval()

        try:
            self.clean(start=start, length=length)
        except ValidationError as e:
            return JsonResponse(dict(
                success=False,
                message=e.message
            ))

        self.object.date = start
        self.object.length = length
        self.object.save(update_fields=['date', 'length'])
        return JsonResponse(dict(success=True, message=_('Event successfully replanned.')))

    def get_object(self) -> BaseEventModel:
        for model in self.models:
            try:
                return get_object_or_404(model, pk=self.request_json.get('id'))
            except Http404:
                pass
        raise Http404

    def clean(self, start: datetime, length: timedelta):
        for executor in self.object.get_executors():
            conflict_feeding, conflict_cleaning = executor.find_in_time(
                start=start,
                length=self.object.length,
            )

            if conflict_feeding.exclude(
                    pk=self.object.pk
            ).exists() or conflict_cleaning.exclude(
                pk=self.object.pk
            ).exists():
                raise ValidationError(_('Reverted, conflict in time plan of executor {}.').format(executor))

        if self.object.date < timezone.now():
            raise ValidationError(_('Reverted, cannot change historical or already started event.'))

        if start < timezone.now():
            raise ValidationError(_('Reverted, cannot move event to history.'))

        if self.object.done:
            raise ValidationError(_('Reverted, cannot move already done event.'))

    def get_interval(self) -> Tuple[datetime, timedelta]:
        raise NotImplementedError


class CalendarEventStartChangeView(BaseCalendarEventChangeView):
    def get_interval(self):
        return parser.parse(self.request_json.get('start')).astimezone(pytz.utc), self.object.length


class CalendarEventEndChangeView(BaseCalendarEventChangeView):
    def get_interval(self):
        return (
            self.object.date,
            parser.parse(self.request_json.get('end')).astimezone(pytz.utc) - self.object.date
        )

    def clean(self, start: datetime, length: timedelta):
        super().clean(start=start, length=length)

        if isinstance(self.object, Cleaning):
            if length < self.object.enclosure.min_cleaning_duration:
                raise ValidationError(_('Reverted, {} is the minimal duration of cleaning {}.').format(
                    self.object.enclosure.min_cleaning_duration,
                    self.object.enclosure
                ))
