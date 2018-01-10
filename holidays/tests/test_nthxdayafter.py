from __future__ import unicode_literals

import datetime

from django.test import TestCase

from holidays.models import NthXDayAfterHoliday, Holiday

class NthXDayAfterHolidayTest(TestCase):
    def setUp(self):
        self.electionday = NthXDayAfterHoliday.objects.create(
            name="Election Day",
            month=11, # November
            nth=1,
            day_of_week=1, # Tuesday
            after_nth=1,
            after_day_of_week=0, # Monday
            paid_holiday=False,
        )
        self.blackfriday = NthXDayAfterHoliday.objects.create(
            name="Black Friday",
            month=11, # November
            nth=1,
            day_of_week=4, # Friday
            after_nth=4,
            after_day_of_week=3, # Thursday
            paid_holiday=True,
        )

    def test_get_holidays(self):
        self.assertListEqual(
            list(Holiday.get_available_holidays()),
            ['Election Day', 'Black Friday'])

    def test_holiday_json(self):
        self.assertDictEqual(
            self.electionday.to_json(2018),
            {
                'id': self.electionday.pk,
                'name': 'Election Day',
                'date': datetime.date(year=2018, month=11, day=6),
                'paid': False,
                'type': 'Nth X Day After Holiday',
            })
        self.assertDictEqual(
            self.blackfriday.to_json(2018),
            {
                'id': self.blackfriday.pk,
                'name': 'Black Friday',
                'date': datetime.date(year=2018, month=11, day=23),
                'paid': True,
                'type': 'Nth X Day After Holiday',
            })

    def test_get_holidays_year(self):
        holidays = Holiday.get_holidays_for_year(2017)
        self.assertEqual(len(holidays), 2)
        self.assertListEqual(holidays, [
            self.electionday.to_json(2017),
            self.blackfriday.to_json(2017),
        ])

        holidays = Holiday.get_holidays_for_year(2018)
        self.assertEqual(len(holidays), 2)
        self.assertListEqual(holidays, [
            self.electionday.to_json(2018),
            self.blackfriday.to_json(2018),
        ])

        holidays = Holiday.get_holidays_for_year(2019)
        self.assertEqual(len(holidays), 2)
        self.assertListEqual(holidays, [
            self.electionday.to_json(2019),
            self.blackfriday.to_json(2019),
        ])

    def test_holidays_between_dates(self):
        start_date = datetime.date(year=2017, month=1, day=1)
        end_date = datetime.date(year=2017, month=12, day=31)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 2)
        self.assertListEqual(holidays, [
            self.electionday.to_json(2017),
            self.blackfriday.to_json(2017),
        ])

        end_date = datetime.date(year=2018, month=11, day=6)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 3)
        self.assertListEqual(holidays, [
            self.electionday.to_json(2017),
            self.blackfriday.to_json(2017),
            self.electionday.to_json(2018),
        ])

        start_date = datetime.date(year=2016, month=1, day=19)
        end_date = datetime.date(year=2016, month=9, day=4)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 0)

    def test_is_holiday(self):
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2016, month=11, day=8)),
            [self.electionday.to_json(2016)])
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2017, month=11, day=7)),
            [self.electionday.to_json(2017)])
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2018, month=11, day=6)),
            [self.electionday.to_json(2018)])

        self.assertFalse(Holiday.is_holiday(datetime.date(year=2016, month=11, day=7)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=11, day=6)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2018, month=11, day=7)))

    def test_is_paid_holiday(self):
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2016, month=11, day=8)))
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=11, day=7)))

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=11, day=24)),
            [self.blackfriday.to_json(2017)])

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2018, month=11, day=23)),
            [self.blackfriday.to_json(2018)])
