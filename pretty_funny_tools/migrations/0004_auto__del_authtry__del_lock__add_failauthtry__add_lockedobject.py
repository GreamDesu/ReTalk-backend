# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AuthTry'
        db.delete_table(u'pretty_funny_tools_authtry')

        # Deleting model 'Lock'
        db.delete_table(u'pretty_funny_tools_lock')

        # Adding model 'FailAuthTry'
        db.create_table(u'pretty_funny_tools_failauthtry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('try_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'pretty_funny_tools', ['FailAuthTry'])

        # Adding model 'LockedObject'
        db.create_table(u'pretty_funny_tools_lockedobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('time_when_can_try_again', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 10, 0, 0))),
        ))
        db.send_create_signal(u'pretty_funny_tools', ['LockedObject'])


    def backwards(self, orm):
        # Adding model 'AuthTry'
        db.create_table(u'pretty_funny_tools_authtry', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('try_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'pretty_funny_tools', ['AuthTry'])

        # Adding model 'Lock'
        db.create_table(u'pretty_funny_tools_lock', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_when_can_try_again', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 9, 0, 0))),
        ))
        db.send_create_signal(u'pretty_funny_tools', ['Lock'])

        # Deleting model 'FailAuthTry'
        db.delete_table(u'pretty_funny_tools_failauthtry')

        # Deleting model 'LockedObject'
        db.delete_table(u'pretty_funny_tools_lockedobject')


    models = {
        u'pretty_funny_tools.failauthtry': {
            'Meta': {'object_name': 'FailAuthTry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'try_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'pretty_funny_tools.lockedobject': {
            'Meta': {'object_name': 'LockedObject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'time_when_can_try_again': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 10, 0, 0)'})
        }
    }

    complete_apps = ['pretty_funny_tools']