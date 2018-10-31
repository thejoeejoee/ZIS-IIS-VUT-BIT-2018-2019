# coding=utf-8
from django.urls import path

from ziscz.web.views.animal import AnimalListView, AnimalDetailView, AnimalCreateView
from ziscz.web.views.auth import LoginView
from ziscz.web.views.calendar import CalendarView
from ziscz.web.views.cleaning import CleaningDetailView, CleaningCreateView
from ziscz.web.views.enclosure import EnclosureListView, EnclosureDetailView, EnclosureCreateView
from ziscz.web.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('animal', AnimalListView.as_view(), name='animal_list'),
    path('animal/create', AnimalCreateView.as_view(), name='animal_create'),
    path('animal/<uuid:pk>', AnimalDetailView.as_view(), name='animal_detail'),

    path('enclosure', EnclosureListView.as_view(), name='enclosure_list'),
    path('enclosure/create', EnclosureCreateView.as_view(), name='enclosure_create'),
    path('enclosure/<uuid:pk>', EnclosureDetailView.as_view(), name='enclosure_detail'),

    path('cleaning/create', CleaningCreateView.as_view(), name='cleaning_create'),
    path('cleaning/<uuid:pk>', CleaningDetailView.as_view(), name='cleaning_detail'),

    path('calendar', CalendarView.as_view(), name='calendar'),

    path('login', LoginView.as_view(), name='login'),
]
