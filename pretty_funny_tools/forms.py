from django.contrib.auth.forms import AuthenticationForm

try:
    from captcha.fields import CaptchaField
except ImportError:
    pass


class PrettyAuthForm(AuthenticationForm):
    try:
        capcha = CaptchaField()
    except NameError:
        pass
