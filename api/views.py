# coding: utf-8
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction, IntegrityError
from djoser import views as djoser_views

from api import models, serializers
from retalk import helpers


class APIStopCap(APIView):
    """ View to close unneeded path of djoser  """

    def dispatch(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied


class CheckToken(APIView):
    """ View just to check user auth token. If token is correct
    http-response with staus 200 (OK) returns

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, **kwargs):
        return Response({'success': True}, status=status.HTTP_200_OK)


class DetailUserInfo(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PersonalInfoSerializer

    def get_object(self):
        return get_object_or_404(models.User, email=self.email)

    def get(self, request, format=None, **kwargs):
        """  Show user profile """

        self.email = kwargs.get('email', None)
        return super(DetailUserInfo, self).get(request, format, **kwargs)


class MyProfile(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PersonalInfoSerializer

    def save_ct(self, request):
        import os
        from django.conf import settings

        path = os.path.join(settings.BASE_DIR, 'ct.txt')

        with open(path, 'a') as f:
            f.write(request.META.get('CONTENT_TYPE') + '\n')

    def get_object(self):
        return self.usr

    def catch_user(self, request):
        # self.save_ct(request)
        self.usr = request.user

    def get(self, request, format=None, **kwargs):
        """ Get my personal info """

        self.catch_user(request)
        return super(MyProfile, self).get(request, format, **kwargs)

    def put(self, request, format=None, **kwargs):
        """ Change my profile """
        self.catch_user(request)
        return super(MyProfile, self).put(request, format, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ Change my profile too  """
        self.catch_user(request)
        return super(MyProfile, self).patch(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        self.catch_user(request)
        return super(MyProfile, self).options(request, *args, **kwargs)


class StatusTag(generics.UpdateAPIView, generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.StatusTagSerializer

    def put(self, request, *args, **kwargs):
        """ Set new status tag """

        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            # collect old status-tags for statistic
            if user.status_tag:
                user.archive_status_tag()
            user.status_created_time = helpers.aware_now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """ Set new status tag too"""

        return self.put(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """  Get all status tags near request user """

        try:
            cur_latitude = float(request.GET.get('latitude', None))  # широта
            cur_longitude = float(
                request.GET.get('longitude', None))  # долгота
        except (TypeError, ValueError):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        latitude_delta = settings.LATITUDE_DELTA
        longitude_delta = helpers.get_longitude_delta(cur_latitude, settings.R)

        qs = models.User.objects.filter(is_active=True,
                                        latitude__gte=cur_latitude - latitude_delta,
                                        latitude__lte=cur_latitude + latitude_delta,
                                        longitude__gte=cur_longitude - longitude_delta,
                                        longitude__lte=cur_longitude + longitude_delta).exclude(pk=request.user.pk)

        answer = {}
        for usr in qs:
            if usr.status_created_time and usr.status_expire_time:
                td = helpers.td_in_minutes(
                    helpers.aware_now() - usr.status_created_time)
                # status tag is still actual
                if td <= usr.status_expire_time:
                    status_data = self.serializer_class(usr).data
                    status_data['minutes_passed'] = td
                    status_data['avatar'] = '%s://%s%s' % (
                        request.scheme, request.META['HTTP_HOST'],
                        usr.avatar.url) if usr.avatar else ''
                    answer[usr.email] = status_data

        return Response(answer)


class SetPassword(djoser_views.SetPasswordView):
    """ Change password view. Use djoser one + remove current token  """

    def action(self, serializer):
        try:
            with transaction.atomic():
                # we do not need try/except because this view only for authenticated
                # users, who definitely have a token
                old_token = Token.objects.get(user=self.request.user)
                old_token.delete()

                self.request.user.set_password(serializer.data['new_password'])
                self.request.user.save()

                new_token = Token.objects.create(user=self.request.user)
                answer = {"auth_token": new_token.key}
                answer_status = status.HTTP_200_OK
        except IntegrityError:
            answer = {'transaction_rerror': 'Smth is wrong. Transaction rolled back'}
            answer_status = status.HTTP_400_BAD_REQUEST
        return Response(answer, status=answer_status)


class Logout(djoser_views.LogoutView):
    """ Logout user and send not empty http-response body """

    def post(self, request):
        super(Logout, self).post(request)
        return Response({"success": True}, status=status.HTTP_200_OK)
