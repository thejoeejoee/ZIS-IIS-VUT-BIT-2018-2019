# coding=utf-8
from django.urls import path

from ziscz.api.views.calendar import CleaningCalendarView, FeedingCalendarView, CalendarEventStartChangeView, \
    CalendarEventEndChangeView

urlpatterns = [
    path('calendar/cleaning', CleaningCalendarView.as_view(), name='calendar_cleaning'),
    path('calendar/feeding', FeedingCalendarView.as_view(), name='calendar_feeding'),

    path('calendar/event-start-change', CalendarEventStartChangeView.as_view(), name='calendar_event_start_change'),
    path('calendar/event-end-change', CalendarEventEndChangeView.as_view(), name='calendar_event_end_change'),
]

app_name = 'api'
