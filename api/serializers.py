from rest_framework import serializers

from api import models


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('nickname', 'gender', 'birthday', 'link', 'about', 'avatar')


class StatusTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('nickname', 'status_tag', 'status_tag_background_num', 'latitude', 'longitude', 'extra_description',
                  'status_expire_time')
