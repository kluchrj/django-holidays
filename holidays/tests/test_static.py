from __future__ import unicode_literals

import datetime

from django.test import TestCase

from holidays.models import Holiday, StaticHoliday

class StaticHolidayTest(TestCase):
    def setUp(self):
        self.christmas = StaticHoliday.objects.create(
            name="Christmas",
            month=12, # December
            day=25,
            paid_holiday=True,
        )
        self.christmas_eve = StaticHoliday.objects.create(
            name="Christmas Eve",
            month=12, # December
            day=24,
            paid_holiday=False,
        )
        self.new_years = StaticHoliday.objects.create(
            name="New Year's Day",
            month=1, # January
            day=1,
            paid_holiday=True,
        )
        self.new_years_eve = StaticHoliday.objects.create(
            name="New Year's Eve",
            month=12, # December
            day=31,
            paid_holiday=False,
        )

    def test_get_holidays(self):
        self.assertListEqual(
            list(Holiday.get_available_holidays()),
            ['Christmas', 'Christmas Eve', 'New Year\'s Day', 'New Year\'s Eve'])

    def test_holiday_json(self):
        self.assertDictEqual(
            self.christmas.to_json(),
            {
                'id': self.christmas.pk,
                'name': 'Christmas',
                'date': datetime.date(datetime.date.today().year, month=12, day=25),
                'paid': True,
                'type': 'Static Holiday',
            })
        self.assertDictEqual(
            self.christmas_eve.to_json(),
            {
                'id': self.christmas_eve.pk,
                'name': 'Christmas Eve',
                'date': datetime.date(datetime.date.today().year, month=12, day=24),
                'paid': False,
                'type': 'Static Holiday',
            })
        self.assertDictEqual(
            self.new_years.to_json(),
            {
                'id': self.new_years.pk,
                'name': 'New Year\'s Day',
                'date': datetime.date(datetime.date.today().year, month=1, day=1),
                'paid': True,
                'type': 'Static Holiday',
            })
        self.assertDictEqual(
            self.new_years_eve.to_json(),
            {
                'id': self.new_years_eve.pk,
                'name': 'New Year\'s Eve',
                'date': datetime.date(datetime.date.today().year, month=12, day=31),
                'paid': False,
                'type': 'Static Holiday',
            })

    def test_get_holidays_year(self):
        holidays = Holiday.get_holidays_for_year(2017)
        self.assertEqual(len(holidays), 4)
        self.assertListEqual(holidays, [
            self.new_years.to_json(2017),
            self.christmas_eve.to_json(2017),
            self.christmas.to_json(2017),
            self.new_years_eve.to_json(2017),
        ])

        holidays = Holiday.get_holidays_for_year(2018)
        self.assertEqual(len(holidays), 4)
        self.assertListEqual(holidays, [
            self.new_years.to_json(2018),
            self.christmas_eve.to_json(2018),
            self.christmas.to_json(2018),
            self.new_years_eve.to_json(2018),
        ])

        holidays = Holiday.get_holidays_for_year(2019)
        self.assertEqual(len(holidays), 4)
        self.assertListEqual(holidays, [
            self.new_years.to_json(2019),
            self.christmas_eve.to_json(2019),
            self.christmas.to_json(2019),
            self.new_years_eve.to_json(2019),
        ])

    def test_holidays_between_dates(self):
        start_date = datetime.date(year=2017, month=1, day=1)
        end_date = datetime.date(year=2017, month=12, day=31)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 4)
        self.assertListEqual(holidays, [
            self.new_years.to_json(2017),
            self.christmas_eve.to_json(2017),
            self.christmas.to_json(2017),
            self.new_years_eve.to_json(2017),
        ])

        end_date = datetime.date(year=2018, month=12, day=24)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 6)
        self.assertListEqual(holidays, [
            self.new_years.to_json(2017),
            self.christmas_eve.to_json(2017),
            self.christmas.to_json(2017),
            self.new_years_eve.to_json(2017),
            self.new_years.to_json(2018),
            self.christmas_eve.to_json(2018),
        ])

        start_date = datetime.date(year=2016, month=1, day=2)
        end_date = datetime.date(year=2016, month=12, day=23)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 0)

    def test_is_holiday(self):
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2017, month=1, day=1)),
            [self.new_years.to_json(2017)])

        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=1, day=2)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=12, day=23)))

    def test_is_paid_holiday(self):
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=12, day=24)))
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=12, day=31)))

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=1, day=1)),
            [self.new_years.to_json(2017),])

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=12, day=25)),
            [self.christmas.to_json(2017),])
