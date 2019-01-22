from django.shortcuts import render
import django.views.generic as generic_views
from time import sleep
from django.core.urlresolvers import reverse

# Create your views here.
from django.contrib.auth.models import User, check_password


class JoomlaAdminView(generic_views.TemplateView):
    template_name = 'fakes/joomla/joomla_admin.html'


class JoomlaAdminFailView(generic_views.TemplateView):
    # template_name = 'fakes/joomla/joomla_admin_fake.html'

    def dispatch(self, request, *args, **kwargs):
        return super(JoomlaAdminFailView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        sleep(1)
        return 'fakes/joomla/joomla_admin_fake.html'


class WPAdminView(generic_views.TemplateView):
    template_name = 'fakes/wp/wp.html'

    def dispatch(self, request, *args, **kwargs):
        return super(WPAdminView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WPAdminView, self).get_context_data(**kwargs)
        sleep(1)
        if self.request.method == 'POST':
            context['show_error'] = True
        else:
            context['show_error'] = False
        return context
