# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from django.forms import Form, ModelForm


class BaseLayoutFormMixin(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class BaseForm(BaseLayoutFormMixin, Form):
    pass


class BaseModelForm(BaseLayoutFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        self.updating = bool(kwargs.get('instance'))
        super().__init__(*args, **kwargs)
