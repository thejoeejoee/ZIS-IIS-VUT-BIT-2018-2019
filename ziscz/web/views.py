# coding=utf-8
# Create your views here.
from django.views.generic import TemplateView


class AppView(TemplateView):
    template_name = 'web/app.html'
