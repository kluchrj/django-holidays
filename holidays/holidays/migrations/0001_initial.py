# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('month', models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('paid_holiday', models.BooleanField(default=False, help_text='If using this app for a business, is the holiday a paid holiday?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomHoliday',
            fields=[
                ('holiday_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='holidays.Holiday')),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('year', models.PositiveSmallIntegerField()),
            ],
            bases=('holidays.holiday',),
        ),
        migrations.CreateModel(
            name='NthXDayAfterHoliday',
            fields=[
                ('holiday_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='holidays.Holiday')),
                ('nth', models.PositiveSmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth')])),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('after_nth', models.PositiveSmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth')])),
                ('after_day_of_week', models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
            ],
            bases=('holidays.holiday',),
        ),
        migrations.CreateModel(
            name='NthXDayHoliday',
            fields=[
                ('holiday_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='holidays.Holiday')),
                ('nth', models.PositiveSmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Last')])),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
            ],
            bases=('holidays.holiday',),
        ),
        migrations.CreateModel(
            name='StaticHoliday',
            fields=[
                ('holiday_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='holidays.Holiday')),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
            ],
            bases=('holidays.holiday',),
        ),
    ]
