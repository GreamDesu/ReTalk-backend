from django.conf.urls import include, url
from django.contrib.auth import get_user_model

from api import views

User = get_user_model()

urlpatterns = [
    # close djoser functions we do not need
    url(r'auth/$', views.APIStopCap.as_view()),
    url(r'auth/me/', views.APIStopCap.as_view()),
    url(r'auth/activate/', views.APIStopCap.as_view()),
    url(r'^{0}/$'.format(User.USERNAME_FIELD), views.APIStopCap.as_view()),
    url(r'^password/reset/$', views.APIStopCap.as_view()),
    url(r'^password/reset/confirm/$', views.APIStopCap.as_view()),

    # override djoser views
    url(r'^auth/password/$', views.SetPassword.as_view(), name='set_password'),
    url(r'^auth/logout/$', views.Logout.as_view(), name='logout'),


    # djoser auth app
    url(r'auth/', include('djoser.urls')),

    # custom
    url(r'check/token/$', views.CheckToken.as_view(), name='check_token'),
    url(r'profile/me/$', views.MyProfile.as_view(), name='my_profile'),
    url(r'profile/(?P<email>.+?)/$', views.DetailUserInfo.as_view(), name='profile'),
    url(r'status/tag/$', views.StatusTag.as_view(), name='status_tag'),

]
