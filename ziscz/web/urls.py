# coding=utf-8
from django.urls import re_path, path

from ziscz.web.views.auth import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
]
