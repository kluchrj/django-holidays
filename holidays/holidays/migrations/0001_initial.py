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
                ('month', models.PositiveSmallIntegerField(choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('paid_holiday', models.BooleanField(default=False, help_text=b'If using this app for a business, is the holiday a paid holiday?')),
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
                ('nth', models.PositiveSmallIntegerField(choices=[(1, b'First'), (2, b'Second'), (3, b'Third'), (4, b'Fourth'), (5, b'Fifth')])),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
                ('after_nth', models.PositiveSmallIntegerField(choices=[(1, b'First'), (2, b'Second'), (3, b'Third'), (4, b'Fourth'), (5, b'Fifth')])),
                ('after_day_of_week', models.PositiveSmallIntegerField(choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
            ],
            bases=('holidays.holiday',),
        ),
        migrations.CreateModel(
            name='NthXDayHoliday',
            fields=[
                ('holiday_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='holidays.Holiday')),
                ('nth', models.PositiveSmallIntegerField(choices=[(1, b'First'), (2, b'Second'), (3, b'Third'), (4, b'Fourth'), (5, b'Last')])),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
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
