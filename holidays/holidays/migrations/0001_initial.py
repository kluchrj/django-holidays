# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Holiday'
        db.create_table(u'holidays_holiday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('month', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'holidays', ['Holiday'])

        # Adding model 'StaticHoliday'
        db.create_table(u'holidays_staticholiday', (
            (u'holiday_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['holidays.Holiday'], unique=True, primary_key=True)),
            ('day', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'holidays', ['StaticHoliday'])

        # Adding model 'NthXDayHoliday'
        db.create_table(u'holidays_nthxdayholiday', (
            (u'holiday_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['holidays.Holiday'], unique=True, primary_key=True)),
            ('nth', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'holidays', ['NthXDayHoliday'])

        # Adding model 'NthXDayAfterHoliday'
        db.create_table(u'holidays_nthxdayafterholiday', (
            (u'holiday_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['holidays.Holiday'], unique=True, primary_key=True)),
            ('nth', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('after_nth', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('after_day_of_week', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'holidays', ['NthXDayAfterHoliday'])

        # Adding model 'CustomHoliday'
        db.create_table(u'holidays_customholiday', (
            (u'holiday_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['holidays.Holiday'], unique=True, primary_key=True)),
            ('day', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'holidays', ['CustomHoliday'])


    def backwards(self, orm):
        # Deleting model 'Holiday'
        db.delete_table(u'holidays_holiday')

        # Deleting model 'StaticHoliday'
        db.delete_table(u'holidays_staticholiday')

        # Deleting model 'NthXDayHoliday'
        db.delete_table(u'holidays_nthxdayholiday')

        # Deleting model 'NthXDayAfterHoliday'
        db.delete_table(u'holidays_nthxdayafterholiday')

        # Deleting model 'CustomHoliday'
        db.delete_table(u'holidays_customholiday')


    models = {
        u'holidays.customholiday': {
            'Meta': {'object_name': 'CustomHoliday', '_ormbases': [u'holidays.Holiday']},
            'day': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'holiday_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['holidays.Holiday']", 'unique': 'True', 'primary_key': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'holidays.holiday': {
            'Meta': {'object_name': 'Holiday'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'holidays.nthxdayafterholiday': {
            'Meta': {'object_name': 'NthXDayAfterHoliday', '_ormbases': [u'holidays.Holiday']},
            'after_day_of_week': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'after_nth': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'day_of_week': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'holiday_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['holidays.Holiday']", 'unique': 'True', 'primary_key': 'True'}),
            'nth': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'holidays.nthxdayholiday': {
            'Meta': {'object_name': 'NthXDayHoliday', '_ormbases': [u'holidays.Holiday']},
            'day_of_week': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'holiday_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['holidays.Holiday']", 'unique': 'True', 'primary_key': 'True'}),
            'nth': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'holidays.staticholiday': {
            'Meta': {'object_name': 'StaticHoliday', '_ormbases': [u'holidays.Holiday']},
            'day': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'holiday_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['holidays.Holiday']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['holidays']