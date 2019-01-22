from django.conf.urls import patterns, url
from django.contrib import admin
import views as pretty_views

# admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^administrator/$', pretty_views.JoomlaAdminView.as_view(), name='joomla_admin'),
                       url(r'^administrator/index.php$', pretty_views.JoomlaAdminFailView.as_view(),
                           name='joomla_admin_fail'),

                       url(r'^wp-login.php$', pretty_views.WPAdminView.as_view(), name='wp_admin'),

                       )
