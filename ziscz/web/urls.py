# coding=utf-8
from django.urls import re_path

from .views import AppView

urlpatterns = [

    re_path('.*', AppView.as_view()),
]
