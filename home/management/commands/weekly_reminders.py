

import pandas as pd

from datetime import date, datetime
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from home.models import Program
from isoweek import Week

from django.conf import settings


class Command(BaseCommand):
    help = 'Imports program data to SQL through API'

    # A command must define handle
    def handle(self, *args, **options):

        # Import Program Data
        engine = create_engine(
            'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))
        df = pd.read_sql_query("select * from program;", con=engine)


        df['year_weeknum'] = zip(df['year'], df['weeknum'])
        df['iso_year_weeknum'] = df['year_weeknum'].map(lambda x: Week(x[0], x[1]))

        year, week, _ = date.today().isocalendar()
        current_week = Week(year, week)

        # since how many week this report is about
        df['since_x_weeks'] = df['iso_year_weeknum'].map(lambda x: current_week - x)

        df.query('since_x_weeks>0').query('since_x_weeks<=8').query('siteid>101110001').groupby(df['siteid'])['weeknum'].unique().map(
            lambda x: list(sorted(set(range(week - 8, week)) - set(x))))
