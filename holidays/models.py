from __future__ import unicode_literals

import calendar
import datetime

from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import BooleanField, Case, Value, Q, When
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Holiday(models.Model):
    STATIC = 'STATIC'
    NXDAY = 'NXDAY'
    NXADAY = 'NXADAY'
    CUSTOM = 'CUSTOM'
    HOLIDAY_TYPES = (
        (STATIC, 'Static Holiday'),
        (NXDAY, 'Nth X Day Holiday'),
        (NXADAY, 'Nth X Day After Holiday'),
        (CUSTOM, 'Custom Holiday'),
    )
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
    DOWS = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    NTHS = {
        1: 'First',
        2: 'Second',
        3: 'Third',
        4: 'Fourth',
        5: 'Fifth',
    }
    DAYS = [(i, i) for i in range(1, 32)]

    name = models.CharField(max_length=64)
    month = models.PositiveSmallIntegerField(choices=MONTHS.items())
    type = models.CharField(max_length=6, choices=HOLIDAY_TYPES, db_index=True)
    paid_holiday = models.BooleanField(
        default=False,
        help_text='If using this app for a business, is the holiday a paid holiday?')

    # Static Holiday
    day = models.PositiveSmallIntegerField(choices=DAYS, blank=True, null=True)
    offset_weekend = models.BooleanField(
        default=False,
        help_text='Offset the date if it falls on a weekend to a weekday?')

    # Nth X Day Holiday
    nth = models.PositiveSmallIntegerField(choices=NTHS.items(), blank=True, null=True)
    day_of_week = models.PositiveSmallIntegerField(choices=DOWS.items(), blank=True, null=True)

    # Nth X Day After Holiday
    after_nth = models.PositiveSmallIntegerField(choices=NTHS.items(), blank=True, null=True)
    after_day_of_week = models.PositiveSmallIntegerField(
        choices=DOWS.items(), blank=True, null=True)

    # Custom Holiday
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, 'PAID' if self.paid_holiday else 'not paid')

    def clean(self):
        if self.type == self.STATIC and self.day is None:
            raise ValidationError('Static Holidays must specify a day.')
        elif self.type == self.NXDAY:
            if self.nth is None:
                raise ValidationError('Nth X Day Holidays must specify a Nth ordinal.')
            if self.day_of_week is None:
                raise ValidationError('Nth X Day Holidays must specify a Day of week.')
        elif self.type == self.NXADAY:
            if self.nth is None:
                raise ValidationError('Nth X Day After Holidays must specify a Nth ordinal.')
            if self.day_of_week is None:
                raise ValidationError('Nth X Day After Holidays must specify a Day of week.')
            if self.after_nth is None:
                raise ValidationError('Nth X Day After Holidays must specify an After nth ordinal.')
            if self.after_day_of_week is None:
                raise ValidationError('Nth X Day After Holidays must specify an After day of week.')
        elif self.type == self.CUSTOM:
            if self.day is None:
                raise ValidationError('Custom Holidays must specify a day.')
            if self.year is None:
                raise ValidationError('Custom Holidays must specify a year.')

    def date(self, year=None):
        """Returns the date of the holiday for the provided year.
        Defaults to the current year."""
        if year is None:
            year = datetime.date.today().year

        if self.type == self.STATIC:
            day = datetime.date(year, self.month, self.day)

            if self.offset_weekend:
                if day.weekday() == 5: # Saturday
                    day -= datetime.timedelta(days=1)
                elif day.weekday() == 6: # Sunday
                    day += datetime.timedelta(days=1)

        elif self.type == self.NXDAY:
            if self.nth < 5:
                count = 0
                day = datetime.date(year, self.month, 1)
                while count < self.nth:
                    if day.weekday() == self.day_of_week:
                        count += 1
                    day += relativedelta(days=1)
                day -= relativedelta(days=1)
            else:
                day = datetime.date(
                    year, self.month, calendar.monthrange(year, self.month)[1])
                while day.weekday() != self.day_of_week:
                    day -= relativedelta(days=1)

        elif self.type == self.NXADAY:
            if self.after_nth < 5:
                count = 0
                after_date = datetime.date(year, self.month, 1)
                while count < self.after_nth:
                    if after_date.weekday() == self.after_day_of_week:
                        count += 1
                    after_date += relativedelta(days=1)
                after_date -= relativedelta(days=1)
            else:
                after_date = datetime.date(
                    year, self.month, calendar.monthrange(year, self.month)[1])
                while after_date.weekday() != self.after_day_of_week:
                    after_date -= relativedelta(days=1)

            day = after_date
            count = 0
            while count < self.nth:
                if day.weekday() == self.day_of_week:
                    count += 1
                day += relativedelta(days=1)
            day -= relativedelta(days=1)

        elif self.type == self.CUSTOM:
            day = datetime.date(self.year, self.month, self.day)

        return day

    def to_json(self, year=None):
        return {
            'id': self.pk,
            'name': self.name,
            'date': self.date(year),
            'paid': self.paid_holiday,
            'type': self.get_type_display(),
        }

    @classmethod
    def get_available_holidays(cls):
        """Returns a list of all holiday names."""
        return cls.objects.all().values_list('name', flat=True).distinct()

    @classmethod
    def get_holidays_for_year(cls, year=None, **kwargs):
        """Returns a list of all holidays for the provided year.
        Defaults to the current year. Kwargs are passed to the Holiday queryset.
        """
        if year is None:
            year = datetime.date.today().year

        holidays = cls.objects.annotate(
            display=Case(
                When(type=cls.STATIC, then=Value(True)),
                When(type=cls.NXDAY, then=Value(True)),
                When(type=cls.NXADAY, then=Value(True)),
                When(Q(type=cls.CUSTOM) & Q(year=year), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).filter(display=True, **kwargs)

        json_holidays = []
        for holiday in holidays:
            json_holidays.append(holiday.to_json(year))

        return sorted(json_holidays, key=lambda x: x['date'])

    @classmethod
    def holidays_between_dates(cls, start_date, end_date, **kwargs):
        """Returns a list of all holidays between start_date and end_date.
        kwargs are passed to the holiday queryset.
        """
        holidays = cls.objects.annotate(
            display=Case(
                When(type=cls.STATIC, then=Value(True)),
                When(type=cls.NXDAY, then=Value(True)),
                When(type=cls.NXADAY, then=Value(True)),
                When(Q(type=cls.CUSTOM) & Q(year__range=(start_date.year, end_date.year)),
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).filter(display=True, **kwargs)

        json_holidays = []
        for year in range(start_date.year, end_date.year + 1):
            for holiday in holidays:
                json = holiday.to_json(year)
                if start_date <= json['date'] <= end_date and json['date'].year == year:
                    json_holidays.append(json)

        return sorted(json_holidays, key=lambda x: x['date'])

    @classmethod
    def is_holiday(cls, date):
        """Determines if the provided date is a holiday.  If so, returns the
        holiday json object.  Otherwise returns False.
        """
        return cls.holidays_between_dates(date, date) or False

    @classmethod
    def is_paid_holiday(cls, date):
        """Determines if the provided date is a paid holiday.  If so, returns the
        holiday json object.  Otherwise returns False.
        """
        return cls.holidays_between_dates(date, date, paid_holiday=True) or False


class StaticHolidayManager(models.Manager):
    def get_queryset(self):
        return super(StaticHolidayManager, self).get_queryset().filter(type=Holiday.STATIC)

class StaticHoliday(Holiday):
    """Static holidays are holidays that have the exact same month/day each year."""

    objects = StaticHolidayManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = Holiday.STATIC
        super(StaticHoliday, self).__init__(*args, **kwargs)


class NthXDayHolidayManager(models.Manager):
    def get_queryset(self):
        return super(NthXDayHolidayManager, self).get_queryset().filter(type=Holiday.NXDAY)

class NthXDayHoliday(Holiday):
    """Holidays that are a specific Nth day of a month.
    Ex. Third Monday or January is MLK Day"""

    objects = NthXDayHolidayManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = Holiday.NXDAY
        super(NthXDayHoliday, self).__init__(*args, **kwargs)


class NthXDayHolidayAfterManager(models.Manager):
    def get_queryset(self):
        return super(NthXDayHolidayAfterManager, self).get_queryset().filter(type=Holiday.NXADAY)

class NthXDayAfterHoliday(Holiday):
    """Holidays that are a specific Nth day of a month AFTER an Nth day of a month.
    Ex. First Tuesday after First Monday in November is USA Election Day"""

    objects = NthXDayHolidayAfterManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = Holiday.NXADAY
        super(NthXDayAfterHoliday, self).__init__(*args, **kwargs)


class CustomHolidayManager(models.Manager):
    def get_queryset(self):
        return super(CustomHolidayManager, self).get_queryset().filter(type=Holiday.CUSTOM)

@python_2_unicode_compatible
class CustomHoliday(Holiday):
    """Holidays that have custom dates for each year."""

    objects = CustomHolidayManager()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = Holiday.CUSTOM
        super(CustomHoliday, self).__init__(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.name, self.year)
