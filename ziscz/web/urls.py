# coding=utf-8
from django.urls import path

from ziscz.web.views.animal import AnimalListView, AnimalDetailView
from ziscz.web.views.auth import LoginView
from ziscz.web.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('animal', AnimalListView.as_view(), name='animal_list'),
    path('animal/<uuid:pk>', AnimalDetailView.as_view(), name='animal_detail'),
    path('login', LoginView.as_view(), name='login'),
]
