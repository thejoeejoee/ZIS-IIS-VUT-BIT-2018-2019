# coding=utf-8
from __future__ import unicode_literals

from ziscz.core.views.forms import BaseFormView
from ..forms.auth import LoginForm


class LoginView(BaseFormView):
    form_class = LoginForm
    url_name = 'login'
