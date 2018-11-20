# coding=utf-8
from django.urls import path

from ziscz.api.views.calendar import CleaningCalendarView, FeedingCalendarView

urlpatterns = [
    path('calendar/cleaning', CleaningCalendarView.as_view(), name='calendar_cleaning'),
    path('calendar/feeding', FeedingCalendarView.as_view(), name='calendar_feeding'),
]

app_name = 'api'