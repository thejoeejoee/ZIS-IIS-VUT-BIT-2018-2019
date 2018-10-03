# coding=utf-8
from __future__ import unicode_literals

from django.forms import Form, ModelForm


class BaseForm(Form):
    pass


class BaseModelForm(ModelForm):
    pass
