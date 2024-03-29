# coding=utf-8
from __future__ import unicode_literals

from django.contrib.messages.views import SuccessMessageMixin as DjangoSuccessMessageMixin
from django.utils.translation import ugettext_lazy as _


class SuccessMessageMixin(DjangoSuccessMessageMixin):
    success_message = _('{instance} was successfully saved.')

    def get_success_message(self, cleaned_data):
        return self.success_message.format(
            instance=self.object,
            **cleaned_data
        )


class SaveAndContinueMixin(object):
    KEY = '_save_and_continue'

    def get_success_url(self):
        if self.request.POST.get(self.KEY):
            return self.request.path
        return super().get_success_url()
