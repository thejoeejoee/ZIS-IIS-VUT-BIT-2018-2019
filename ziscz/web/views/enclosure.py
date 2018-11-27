# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from ziscz.core.models import Enclosure
from ziscz.core.serializers import EnclosureSerializer
from ziscz.core.views.forms import SuccessMessageMixin, SaveAndContinueMixin
from ziscz.web.forms.enclosure import EnclosureForm


class EnclosureListView(PermissionRequiredMixin, ListView):
    template_name = 'web/enclosure_list.html'
    queryset = Enclosure.objects.select_related(
        'type_enclosure',
    )
    allow_empty = True
    permission_required = 'core.view_enclosure'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['data'] = dict(
            enclosures=EnclosureSerializer(context.get('object_list'), many=True).data,
            can_change_animal=self.request.user.has_perm('core.change_animal'),
        )
        return context


class EnclosureDetailView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, UpdateView):
    template_name = 'web/enclosure_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure
    permission_required = 'core.change_enclosure'


class EnclosureCreateView(PermissionRequiredMixin, SuccessMessageMixin, SaveAndContinueMixin, CreateView):
    template_name = 'web/form_detail.html'
    form_class = EnclosureForm
    success_url = reverse_lazy('enclosure_list')
    model = Enclosure
    permission_required = 'core.add_enclosure'
