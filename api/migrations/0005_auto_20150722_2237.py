# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150721_2329'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='user',
            index_together=set([('is_active', 'latitude', 'longitude')]),
        ),
    ]
