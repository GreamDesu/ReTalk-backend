# coding: utf-8
from django.template.loader import render_to_string
import os

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatewords
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from mailqueue.models import MailerMessage
from pytils.translit import slugify as rus_slugify


def make_upload_path(instance, filename):
    name = ''.join(filename.split('.')[:-1])
    ext = filename.split('.')[-1]
    new_filename = str(rus_slugify(name)) + '.' + ext
    return os.path.join('users', new_filename).encode('utf-8')


class UserManager(BaseUserManager):
    """ Queryset manager for application user model """

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(u"Email is empty")

        user = self.model(email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class StatusTagMixin(models.Model):
    """ Status-tag data (abstract model) """

    status_tag = models.CharField('Status-tag', max_length=70, blank=True, help_text='Current status-tag')
    latitude = models.FloatField('Latitude', blank=True, null=True, db_index=True)
    longitude = models.FloatField('Longitude', blank=True, null=True, db_index=True)
    extra_description = models.CharField('Extra geo description', blank=True, max_length=70,
                                         help_text='Extra information about user position')
    status_created_time = models.DateTimeField('Status created time', blank=True, null=True, db_index=True,
                                               help_text='Time when current status-tag was created')
    status_expire_time = models.PositiveIntegerField('Status expire time', blank=True, null=True, db_index=True,
                                                     help_text='Number of minutes to show status-tag')

    class Meta:
        abstract = True


class User(AbstractBaseUser, StatusTagMixin, PermissionsMixin):
    """ Application users """

    GENDERS = (
        (1, 'male'),
        (2, 'female')
    )

    MALE, FEMALE = [i[0] for i in GENDERS]

    # personal info
    email = models.EmailField('Email', max_length=200, unique=True)
    nickname = models.CharField('Nickname', default='Unknown', max_length=32, blank=True)
    gender = models.SmallIntegerField('Gender', blank=True, null=True, choices=GENDERS)
    birthday = models.DateField('Date of birth', null=True, blank=True)
    link = models.URLField('Personal link', help_text='External personal link. Should contain prefix http or https: '
                                                      'http://about.me.com', blank=True)
    about = models.TextField('About me', blank=True, help_text='Some text about user')
    avatar = models.ImageField('Avatar', upload_to=make_upload_path, blank=True)
    joined_at = models.DateTimeField('Joined at', auto_now_add=True, help_text='Time when user starts use service')

    # monetization
    is_premium = models.BooleanField('Is premium', default=False, help_text='Does user has premium account?')
    # number 1 is default free style
    status_tag_background_num = models.PositiveIntegerField('Status-tag background', default=1)

    # technical info
    is_staff = models.BooleanField('Is staff', default=False,
                                   help_text='Designates whether the user can log into this admin '
                                             'site.')
    is_active = models.BooleanField('Is active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'
        index_together = ('is_active', 'latitude', 'longitude')

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.nickname or self.email

    def archive_status_tag(self):
        StatusTagArchive.objects.create(user=self, status_tag=self.status_tag, latitude=self.latitude,
                                        longitude=self.longitude, extra_description=self.extra_description,
                                        status_created_time=self.status_created_time,
                                        status_expire_time=self.status_expire_time)

    def __unicode__(self):
        return self.get_short_name()


@receiver(post_save, sender=User)
def send_greeting_email(instance, **kwargs):
    is_new = kwargs.get('created', None)
    if is_new:
        new_message = MailerMessage()
        new_message.subject = u"Спасибо за регистрацию!"
        new_message.to_address = instance.email
        # new_message.bcc_address = "myblindcarboncopy@yo.com"
        new_message.from_address = "no-reply@retalk.ca"
        new_message.html_content = render_to_string('email/greeting.html')
        new_message.content = new_message.html_content
        # new_message.app = "Name of your App that is sending the email."
        new_message.do_not_send = True
        new_message.save()


class StatusTagArchive(StatusTagMixin):
    """ Archive for status-tags """

    user = models.ForeignKey(User, verbose_name='User')

    class Meta:
        verbose_name_plural = 'Status-tags(archive)'
        verbose_name = 'status-tag'

    def __unicode__(self):
        return truncatewords(self.status_tag, 7)
