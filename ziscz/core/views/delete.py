# coding=utf-8
from __future__ import unicode_literals

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView as DjDeleteView


class DeleteView(DjDeleteView):
    def delete(self, request, *args, **kwargs):
        msg = _('Object {} was deleted.').format(str(self.get_object()))
        resp = super().delete(request, *args, **kwargs)
        messages.success(request, msg)
        return resp
