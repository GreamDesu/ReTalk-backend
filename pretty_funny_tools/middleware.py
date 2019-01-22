import models as pretty_models
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now


class PrettyAuthMiddleware(object):
    """ Anti brute force middleware """

    def process_request(self, request):
        current_url = resolve(request.path_info).url_name
        if current_url in settings.LOGIN_VIEWS and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            try:
                person = pretty_models.LockedObject.objects.get(ip=ip)
                if now() < person.time_when_can_try_again:
                    raise PermissionDenied
            except pretty_models.LockedObject.DoesNotExist:
                pretty_models.LockedObject.objects.create(ip=ip)
        return

    def process_response(self, request, response):
        try:
            current_url = resolve(request.path_info).url_name
            if current_url in settings.LOGIN_VIEWS and request.method == 'POST':
                if not request.user.is_authenticated():
                    ip = request.META.get('REMOTE_ADDR')
                    fail_auth = pretty_models.FailAuthTry(ip=ip)
                    fail_auth.save()
        except:
            pass
        return response
