from __future__ import unicode_literals

import datetime

from django.test import TestCase

from holidays.models import CustomHoliday, Holiday

class CustomHolidayTest(TestCase):
    def setUp(self):
        self.easter_2018 = CustomHoliday.objects.create(
            name="Easter",
            month=4, # April
            day=1,
            year=2018,
        )
        self.easter_2017 = CustomHoliday.objects.create(
            name="Easter",
            month=3, # March
            day=16,
            year=2017,
        )
        self.easter_2016 = CustomHoliday.objects.create(
            name="Easter",
            month=3, # March
            day=27,
            year=2016,
        )

    def test_get_holidays(self):
        self.assertListEqual(list(Holiday.get_available_holidays()), ["Easter"])

    def test_holiday_json(self):
        self.assertDictEqual(
            self.easter_2016.to_json(),
            {
                'id': self.easter_2016.pk,
                'name': 'Easter',
                'date': datetime.date(year=2016, month=3, day=27),
                'paid': False,
                'type': 'Custom Holiday',
            })
        self.assertDictEqual(
            self.easter_2017.to_json(),
            {
                'id': self.easter_2017.pk,
                'name': 'Easter',
                'date': datetime.date(year=2017, month=3, day=16),
                'paid': False,
                'type': 'Custom Holiday',
            })
        self.assertDictEqual(
            self.easter_2018.to_json(),
            {
                'id': self.easter_2018.pk,
                'name': 'Easter',
                'date': datetime.date(year=2018, month=4, day=1),
                'paid': False,
                'type': 'Custom Holiday',
            })

    def test_get_holidays_year(self):
        holidays = Holiday.get_holidays_for_year(2017)
        self.assertEqual(len(holidays), 1)
        self.assertDictEqual(holidays[0], self.easter_2017.to_json())

        holidays = Holiday.get_holidays_for_year(2018)
        self.assertEqual(len(holidays), 1)
        self.assertDictEqual(holidays[0], self.easter_2018.to_json())

        holidays = Holiday.get_holidays_for_year(2019)
        self.assertEqual(len(holidays), 0)

    def test_holidays_between_dates(self):
        start_date = datetime.date(year=2017, month=3, day=16)
        end_date = datetime.date(year=2018, month=3, day=31)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 1)
        self.assertDictEqual(holidays[0], self.easter_2017.to_json())

        end_date = datetime.date(year=2018, month=4, day=1)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 2)
        self.assertListEqual(holidays, [self.easter_2017.to_json(), self.easter_2018.to_json()])

        start_date = datetime.date(year=2016, month=3, day=28)
        end_date = datetime.date(year=2017, month=3, day=15)
        holidays = Holiday.holidays_between_dates(start_date, end_date)
        self.assertEqual(len(holidays), 0)

    def test_is_holiday(self):
        self.assertEqual(
            Holiday.is_holiday(datetime.date(year=2017, month=3, day=16)),
            [self.easter_2017.to_json()])

        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=3, day=15)))
        self.assertFalse(Holiday.is_holiday(datetime.date(year=2017, month=3, day=17)))

    def test_is_paid_holiday(self):
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=3, day=15)))
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=3, day=16)))
        self.assertFalse(Holiday.is_paid_holiday(datetime.date(year=2017, month=3, day=17)))

        self.easter_2017.paid_holiday = True
        self.easter_2017.save()

        self.assertEqual(
            Holiday.is_paid_holiday(datetime.date(year=2017, month=3, day=16)),
            [self.easter_2017.to_json()])
