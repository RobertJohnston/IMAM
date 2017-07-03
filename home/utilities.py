# utilities to use in views.py

from datetime import date, timedelta
from raven.contrib.django.raven_compat.models import client


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta


# Beware of week 52 of 2016 when presented as 2017 (first week of year)
def iso_to_gregorian(iso_year, iso_week, iso_day=1):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return int((year_start + timedelta(days=iso_day - 1, weeks=iso_week - 1)).strftime('%s') + '000')


# Code to calculate the last weeknum for any given year (some years have 52 others have 53)
def weeks_for_year(year):
    last_week = date(year, 12, 28)
    return last_week.isocalendar()[1]


def clean(value_to_clean):
    try:
        return int(float(value_to_clean))
    except (ValueError, TypeError):
        print("Fail to convert '%s' as a number" % (value_to_clean))
        return None


def exception_to_sentry(func):
    def _wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            client.captureException()
            raise

    return _wrap