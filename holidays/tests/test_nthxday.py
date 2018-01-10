from __future__ import unicode_literals

import datetime

from django.test import TestCase

from holidays.models import NthXDayHoliday, Holiday

class NthXDayHolidayTest(TestCase):
    def setUp(self):
        self.mlkday = NthXDayHoliday.objects.create(
            name="MLK Day",
            month=1, # January
            nth=3,
            day_of_week=0, # Monday
            paid_holiday=False,
        )
        self.laborday = NthXDayHoliday.objects.create(
            name="Labor Day",
            month=9, # September
            nth=1,
            day_of_week=0, # Monday
            paid_holiday=True,
        )
        self.thanksgiving = NthXDayHoliday.objects.create(
            name="Thanksgiving",
            month=11, # November
            nth=4,
            day_of_week=3, # Thursday
            paid_holiday=True,
        )

    def test_get_holidays(self):
        self.assertListEqual(
            list(Holiday.get_available_holidays()),
            ['MLK Day', 'Labor Day', 'Thanksgiving'])

    def test_holiday_json(self):
        self.assertDictEqual(
            self.mlkday.to_json(2016),
            {
                'id': self.mlkday.pk,
                'name': 'MLK Day',
                'date': datetime.date(year=2016, month=1, day=18),
                'paid': False,
                'type': 'Nth X Day Holiday',
            })
        self.assertDictEqual(
            self.laborday.to_json(2016),
            {
                'id': self.laborday.pk,
                'name': 'Labor Day',
                'date': datetime.date(year=2016, month=9, day=5),
                'paid': True,
                'type': 'Nth X Day Holiday',
            })
        self.assertDictEqual(
            self.thanksgiving.to_json(2016),
            {
                'id': self.thanksgiving.pk,
                'name': 'Thanksgiving',
                'date': datetime.date(year=2016, month=11, day=24),
                'paid': True,
                'type': 'Nth X Day Holiday',
            })

    def test_get_holidays_year(self):
        holidays = Holiday.get_holidays_for_year(2017)
        self.assertEqual(len(holidays), 3)
        self.assertListEqual(holidays, [
            self.mlkday.to_json(2017),
            self.laborday.to_json(2017),
            self.thanksgiving.to_json(2017),
        ])

        holidays = Holiday.get_holidays_for_year(2018)
        self.assertEqual(len(holidays), 3)
        self.assertListEqual(holidays, [
            self.mlkday.to_json(2018),
            self.laborday.to_json(2018),
            self.thanksgiving.to_json(2018),
        ])

        holidays = Holiday.get_holidays_for_year(2019)
        self.assertEqual(len(holidays), 3)
        self.assertListEqual(holidays, [
            self.mlkday.to_json(2019),
            self.laborday.to_json(2019),
            self.thanksgiving.to_json(2019),
        ])

    def test_holidays_between_dates(self):
        start_date = datetime.date(year=2017, month=1, day=1)
        end_date = datetime.date(year=2017, month=12, day=31)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 3)
        self.assertListEqual(holidays, [
            self.mlkday.to_json(2017),
            self.laborday.to_json(2017),
            self.thanksgiving.to_json(2017),
        ])

        end_date = datetime.date(year=2018, month=9, day=4)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 5)
        self.assertListEqual(holidays, [
            self.mlkday.to_json(2017),
            self.laborday.to_json(2017),
            self.thanksgiving.to_json(2017),
            self.mlkday.to_json(2018),
            self.laborday.to_json(2018),
        ])

        start_date = datetime.date(year=2016, month=1, day=19)
        end_date = datetime.date(year=2016, month=9, day=4)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 0)

    def test_is_holiday(self):
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2016, month=11, day=24)),
            [self.thanksgiving.to_json(2016)])
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2017, month=11, day=23)),
            [self.thanksgiving.to_json(2017)])
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2018, month=11, day=22)),
            [self.thanksgiving.to_json(2018)])

        self.assertFalse(Holiday.is_holiday(datetime.date(year=2016, month=11, day=23)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=11, day=24)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2018, month=11, day=23)))

    def test_is_paid_holiday(self):
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2016, month=1, day=18)))
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=1, day=16)))

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=9, day=4)),
            [self.laborday.to_json(2017)])

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=11, day=23)),
            [self.thanksgiving.to_json(2017)])
