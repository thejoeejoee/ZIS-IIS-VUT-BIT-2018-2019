# coding=utf-8
from __future__ import unicode_literals

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView as DjDeleteView


class DeleteView(DjDeleteView):
    template_name = 'web/object_delete.html'

    def delete(self, request, *args, **kwargs):
        msg = _('Object {} was deleted.').format(str(self.get_object()))
        resp = super().delete(request, *args, **kwargs)
        messages.success(request, msg)
        return resp

    def can_perform_delete(self):
        return True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['can_perform_delete'] = self.can_perform_delete()
        return data
