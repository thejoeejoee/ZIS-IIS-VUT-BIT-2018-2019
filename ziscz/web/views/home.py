# coding=utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView

from ziscz.core.models import Animal
from ziscz.web.forms.animal import AnimalForm


class HomeView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        # TODO: custom form view for animal
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(dict(
            form=AnimalForm(instance=Animal.objects.first())
        ))
        return kwargs
