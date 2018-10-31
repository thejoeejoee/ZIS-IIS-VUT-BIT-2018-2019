# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Enclosure
from ziscz.core.serializers import EnclosureSerializer
from ziscz.core.views.forms import SuccessMessageMixin
from ziscz.web.forms.enclosure import EnclosureForm


class EnclosureListView(ListView):
    template_name = 'web/enclosure_list.html'
    model = Enclosure
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['data'] = dict(
            enclosures=EnclosureSerializer(context.get('object_list'), many=True).data
        )
        return context


class EnclosureDetailView(SuccessMessageMixin, UpdateView):
    template_name = 'web/enclosure_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure


class EnclosureCreateView(SuccessMessageMixin, CreateView):
    template_name = 'web/enclosure_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure
