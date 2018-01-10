from __future__ import unicode_literals

import calendar
import datetime

from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Holiday(models.Model):
    MONTHS = {
        1:  'January',
        2:  'February',
        3:  'March',
        4:  'April',
        5:  'May',
        6:  'June',
        7:  'July',
        8:  'August',
        9:  'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }
    name = models.CharField(max_length=64)
    month = models.PositiveSmallIntegerField(choices=MONTHS.items())
    paid_holiday = models.BooleanField(
        default=False,
        help_text='If using this app for a business, is the holiday a paid holiday?')

    class Meta:
        abstract = False

    def __str__(self):
        return '{} ({})'.format(self.name, 'PAID' if self.paid_holiday else 'not paid')

    @classmethod
    def get_date_for_year(cls, name, year=datetime.date.today().year):
        """Try to determine the date for a given holiday based on name
        and either the provided year or defaults to the current year.
        """
        # check first Custom holidays, holidays that have a custom date
        # for each year
        try:
            holiday = CustomHoliday.objects.get(name=name, year=year)
            return datetime.date(holiday.year, holiday.month, holiday.day)
        except:
            pass

        # next try Static holidays, or holidays that have the exact same
        # month/day each year
        try:
            holiday = StaticHoliday.objects.get(name=name)
            day = datetime.date(year, holiday.month, holiday.day)
            if day.weekday() == 5:
                day -= datetime.timedelta(days=1)
            elif day.weekday() == 6:
                day += datetime.timedelta(days=1)
            return day
        except:
            pass

        # next try holidays that are a specific Nth day of a month
        # i.e. Third Monday or January == MLK Day
        try:
            holiday = NthXDayHoliday.objects.get(name=name)
            if holiday.nth < 5:
                count = 0
                date = datetime.date(year, holiday.month, 1)
                while count < holiday.nth:
                    if date.weekday() == holiday.day_of_week:
                        count += 1
                    date += relativedelta(days=1)
                date -= relativedelta(days=1)
                return date
            else:
                date = datetime.date(
                    year, holiday.month, calendar.monthrange(year, holiday.month)[1])
                while date.weekday() != holiday.day_of_week:
                    date -= relativedelta(days=1)
                return date
        except:
            pass

        # next try holidays that are a specific Nth day of a month
        # AFTER an Nth day of a month.
        # i.e. First Tuesday after First Monday in November == USA Election Day
        try:
            holiday = NthXDayAfterHoliday.objects.get(name=name)
            count = 0
            after_date = datetime.date(year, holiday.month, 1)
            while count < holiday.after_nth:
                if after_date.weekday() == holiday.day_of_week:
                    count += 1
                after_date += relativedelta(days=1)
            after_date -= relativedelta(days=1)

            date = after_date
            count = 0
            while count < holiday.nth:
                if date.weekday() == holiday.day_of_week:
                    count += 1
                date += relativedelta(days=1)
            date -= relativedelta(days=1)
            return date
        except:
            pass

        # try to give a useful exception if the holiday is not found.
        # for example, if Easter is a holiday, but just not available for 2020,
        # let's tell the user that rather than saying 'Holiday not found.'
        if Holiday.objects.filter(name=name).count() > 0:
            raise ObjectDoesNotExist(
                'Holiday with that name is found, but cannot determine date for '
                'the provided year. Check your CustomHoliday table.')
        else:
            raise ObjectDoesNotExist('Holiday with that name cannot be found.')

    @classmethod
    def get_available_holidays(cls):
        """Returns a list of all holiday names.
        TODO: could optionally provide a year.
        """
        return Holiday.objects.all().values_list('name', flat=True).distinct()

    @classmethod
    def get_holidays_for_year(cls, year=datetime.date.today().year, kwargs={}):
        """Returns a list of holiday obects for the provided year, defaults
        to the current year.
        """
        holidays = []
        kwargs_year = kwargs.pop('year', datetime.date.today().year)
        for h in StaticHoliday.objects.filter(**kwargs):
            holidays.append(h)
        kwargs.pop('year', datetime.date.today().year)
        for h in NthXDayHoliday.objects.filter(**kwargs):
            holidays.append(h)
        kwargs.pop('year', datetime.date.today().year)
        for h in NthXDayAfterHoliday.objects.filter(**kwargs):
            holidays.append(h)
        kwargs['year'] = year
        for h in CustomHoliday.objects.filter(**kwargs):
            holidays.append(h)

        json_holidays = []
        for holiday in holidays:
            json_holidays.append({
                'name': holiday.name,
                'date': cls.get_date_for_year(holiday.name, year),
                'paid': holiday.paid_holiday,
                'id': holiday.id})
        json_holidays = sorted(json_holidays, key=lambda h: h['date'])
        # TODO: consider using a generator here... since we need them sorted,
        #       probably cannot work.  Although we could sort them above and
        #       have a generator on the to_json part.
        return json_holidays

    @classmethod
    def holidays_between_dates(cls, start_date, end_date, kwargs={}):
        all_holidays = []
        holidays = []
        kwargs_year = kwargs.pop('year', datetime.date.today().year)
        for year in range(start_date.year, end_date.year+1):
            all_holidays.extend(cls.get_holidays_for_year(year=year, kwargs=kwargs))
        for holiday in all_holidays:
            if holiday['date'] >= start_date and holiday['date'] <= end_date:
                holidays.append(holiday)
        return holidays

    @classmethod
    def is_holiday(cls, date):
        """Determines if the provided date is a holiday.  If so, returns the
        holiday object.  Otherwise returns False.
        """
        # TODO: improve how this is done, specifically the second check
        # (after checking the easy StaticHoliday table)

        # check the StaticHoliday to see if the month and day exist in here.
        try:
            h = StaticHoliday.objects.get(month=date.month, day=date.day)
            return dict(h)
        except:
            pass

        # check all other holidays in the year to see if the provided date
        # is a recorded holiday
        for h in cls.get_holidays_for_year(year=date.year):
            if cls.get_date_for_year(name=h['name'], year=date.year) == date:
                return h

        # defaults to returning False
        return False

    @classmethod
    def is_paid_holiday(cls, date):
        """Determines if the provided date is a holiday.  If so, returns the
        holiday object.  Otherwise returns False.
        """
        # TODO: improve how this is done, specifically the second check
        # (after checking the easy StaticHoliday table)

        # checkt the StaticHoliday to see if the month and day exist in here.
        try:
            h = StaticHoliday.objects.get(month=date.month, day=date.day, paid_holiday=True)
            return h
        except:
            pass

        # check all other holidays in the year to see if the provided date
        # is a recorded holiday
        for h in cls.get_holidays_for_year(year=date.year):
            if cls.get_date_for_year(name=h['name'], year=date.year) == date:
                if h['paid']:
                    return h

        # defaults to returning False
        return False

class StaticHoliday(Holiday):
    DAYS = [(i, i) for i in range(1, 32)]

    day = models.PositiveSmallIntegerField(choices=DAYS)


class NthXDayHoliday(Holiday):
    NTHS = {
        1: 'First',
        2: 'Second',
        3: 'Third',
        4: 'Fourth',
        5: 'Last',
    }
    DOWS = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    nth = models.PositiveSmallIntegerField(choices=NTHS.items())
    day_of_week = models.PositiveSmallIntegerField(choices=DOWS.items())


class NthXDayAfterHoliday(Holiday):
    NTHS = {
        1: 'First',
        2: 'Second',
        3: 'Third',
        4: 'Fourth',
        5: 'Fifth',
    }
    DOWS = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    nth = models.PositiveSmallIntegerField(choices=NTHS.items())
    day_of_week = models.PositiveSmallIntegerField(choices=DOWS.items())
    after_nth = models.PositiveSmallIntegerField(choices=NTHS.items())
    after_day_of_week = models.PositiveSmallIntegerField(choices=DOWS.items())


@python_2_unicode_compatible
class CustomHoliday(Holiday):
    DAYS = [(i, i) for i in range(1, 32)]

    def __str__(self):
        return '{} {}'.format(self.name, self.year)

    day = models.PositiveSmallIntegerField(choices=DAYS)
    year = models.PositiveSmallIntegerField()
