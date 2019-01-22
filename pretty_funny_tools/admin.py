from django.contrib import admin
import forms as pretty_forms
from django.conf import settings
import pretty_funny_tools.models as pretty_models
from django.contrib.auth.views import login as django_login

REDIRECT_PARAM_NAME = 'next'
REDIRECT_TO = '/admin/'


def pretty_login(request, *args, **kwargs):
    return django_login(request, template_name='pretty_login.html', authentication_form=pretty_forms.PrettyAuthForm,
                        extra_context={REDIRECT_PARAM_NAME: REDIRECT_TO})


try:
    if settings.USE_CAPTCHA_AT_ADMIN_LOGIN:
        admin.site.login = pretty_login
except AttributeError:
    pass

admin.site.register(pretty_models.FailAuthTry)