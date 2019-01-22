from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from api import models


class AdminUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = models.User
        fields = '__all__'



class AdminUser(UserAdmin):
    form = AdminUserForm
    list_display = ['email', 'nickname', 'gender', 'birthday', 'joined_at', 'is_premium', 'is_staff', 'is_superuser']
    list_filter = ['is_premium', 'joined_at', 'gender', 'is_staff', 'is_superuser', ]
    search_fields = ['email', 'nickname']
    filter_horizontal = ['groups', 'user_permissions']
    ordering = ['email']

    fieldsets = (
        ('Personal info',
         {'fields': ('email', 'nickname', 'avatar', 'gender', 'birthday', 'link', 'about', 'last_login'),
          'classes': ('wide',)}),
        ('Current status-tag', {'fields': (
            'status_tag', ('latitude', 'longitude'), 'extra_description', 'status_created_time', 'status_expire_time'),
            'classes': ('wide',)}),
        ('Monetization', {'fields': ('is_premium', 'status_tag_background_num'), 'classes': ('wide',)}),
        ('Technical info',
         {'fields': ('password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
          'classes': ('wide',)})
    )


class StatusTagArchiveAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'status_created_time']
    search_fields = ['status_tag', 'extra_description']
    list_filter = ['status_created_time']
    readonly_fields = ['status_tag', 'latitude', 'longitude', 'extra_description', 'status_created_time',
                       'status_expire_time']

    fieldsets = (
        (None, {'fields': (
            'status_tag', ('latitude', 'longitude'), 'extra_description', 'status_created_time', 'status_expire_time'),
            'classes': ('wide',)}),
    )

    def get_queryset(self, request):
        qs = super(StatusTagArchiveAdmin, self).get_queryset(request)
        return qs.select_related('user')


admin.site.register(models.User, AdminUser)
admin.site.register(models.StatusTagArchive, StatusTagArchiveAdmin)
