# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('status_tag', models.CharField(help_text=b'Current status-tag', max_length=70, verbose_name=b'Status-tag', blank=True)),
                ('latitude', models.FloatField(db_index=True, null=True, verbose_name=b'Latitude', blank=True)),
                ('longitude', models.FloatField(db_index=True, null=True, verbose_name=b'Longitude', blank=True)),
                ('extra_description', models.CharField(help_text=b'Extra information about user position', max_length=70, verbose_name=b'Extra geo description', blank=True)),
                ('status_created_time', models.DateTimeField(help_text=b'Time when current status-tag was created', null=True, verbose_name=b'Status created time', db_index=True, blank=True)),
                ('status_expire_time', models.PositiveIntegerField(help_text=b'Number of minutes to show status-tag', null=True, verbose_name=b'Status expire time', db_index=True, blank=True)),
                ('email', models.CharField(unique=True, max_length=200, verbose_name=b'Email')),
                ('nickname', models.CharField(default=b'Unknown', max_length=32, verbose_name=b'Nickname', blank=True)),
                ('gender', models.SmallIntegerField(blank=True, null=True, verbose_name=b'Gender', choices=[(1, b'male'), (2, b'female')])),
                ('birthday', models.DateTimeField(null=True, verbose_name=b'Date of birth', blank=True)),
                ('link', models.URLField(help_text=b'External personal link. Should contain prefix http or https: http://about.me.com', verbose_name=b'Personal link', blank=True)),
                ('about', models.TextField(help_text=b'Some text about user', verbose_name=b'About me', blank=True)),
                ('avatar', models.ImageField(upload_to=b'users', verbose_name=b'Avatar', blank=True)),
                ('joined_at', models.DateTimeField(help_text=b'Time when user starts use service', verbose_name=b'Joined at', auto_now_add=True)),
                ('is_premium', models.BooleanField(default=False, help_text=b'Does user has premium account?', verbose_name=b'Is premium')),
                ('status_tag_background_num', models.PositiveIntegerField(default=1, verbose_name=b'Status-tag background')),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'Is staff')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'Is active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='StatusTagArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_tag', models.CharField(help_text=b'Current status-tag', max_length=70, verbose_name=b'Status-tag', blank=True)),
                ('latitude', models.FloatField(db_index=True, null=True, verbose_name=b'Latitude', blank=True)),
                ('longitude', models.FloatField(db_index=True, null=True, verbose_name=b'Longitude', blank=True)),
                ('extra_description', models.CharField(help_text=b'Extra information about user position', max_length=70, verbose_name=b'Extra geo description', blank=True)),
                ('status_created_time', models.DateTimeField(help_text=b'Time when current status-tag was created', null=True, verbose_name=b'Status created time', db_index=True, blank=True)),
                ('status_expire_time', models.PositiveIntegerField(help_text=b'Number of minutes to show status-tag', null=True, verbose_name=b'Status expire time', db_index=True, blank=True)),
                ('user', models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'status-tag',
                'verbose_name_plural': 'Status-tags(archive)',
            },
        ),
    ]
