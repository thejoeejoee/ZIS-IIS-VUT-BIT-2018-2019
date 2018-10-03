# coding=utf-8
from __future__ import unicode_literals

from django.urls import reverse_lazy
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
