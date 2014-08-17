# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Holiday.paid_holiday'
        db.add_column(u'holidays_holiday', 'paid_holiday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Holiday.paid_holiday'
        db.delete_column(u'holidays_holiday', 'paid_holiday')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'paid_holiday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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