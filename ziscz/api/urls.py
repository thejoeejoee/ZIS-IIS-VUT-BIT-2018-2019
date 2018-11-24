# coding=utf-8
from django.urls import path

from ziscz.api.views.calendar import CleaningCalendarView, FeedingCalendarView, CalendarEventStartChangeView, \
    CalendarEventEndChangeView
from ziscz.api.views.enclosure import EnclosureAnimalsSetup

urlpatterns = [
    path('calendar/cleaning', CleaningCalendarView.as_view(), name='calendar_cleaning'),
    path('calendar/feeding', FeedingCalendarView.as_view(), name='calendar_feeding'),

    path('calendar/event-start-change', CalendarEventStartChangeView.as_view(), name='calendar_event_start_change'),
    path('calendar/event-end-change', CalendarEventEndChangeView.as_view(), name='calendar_event_end_change'),

    path('enclosure-animals-setup', EnclosureAnimalsSetup.as_view(), name='enclosure_animals_setup'),
]

app_name = 'api'
