# coding=utf-8
from django.urls import path

from ziscz.web.views.auth import LoginView
from ziscz.web.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
]
