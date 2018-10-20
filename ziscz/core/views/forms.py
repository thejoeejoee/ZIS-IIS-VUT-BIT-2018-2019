# coding=utf-8
from __future__ import unicode_literals

from django.contrib.messages.views import SuccessMessageMixin as DjangoSuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView


class BaseFormView(FormView):
    url_name = None
    template_name = 'core/forms/form.html'

    def get_context_data(self, **kwargs):
        data = super(BaseFormView, self).get_context_data()
        data.update(dict(
            reverse_url=self.get_reverse_url(),
        ))
        return data

    def get_reverse_url(self):
        return reverse_lazy(self.url_name)


class BaseModelFormView(BaseFormView):
    pass


class SuccessMessageMixin(DjangoSuccessMessageMixin):
    success_message = _('{instance} was successfully saved.')

    def get_success_message(self, cleaned_data):
        return self.success_message.format(
            instance=self.object,
            **cleaned_data
        )
