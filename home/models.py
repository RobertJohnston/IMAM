from __future__ import unicode_literals

import uuid
# is this necessary if I am not calling uuid to create uuids?
import datetime
import pandas as pd

from django.db import models
from django.utils import timezone
from django.conf import settings
from sqlalchemy import create_engine


# Put the loading of data in a function and run once when needed.

# Load dataframe - note for contacts  - use 'Contacts' tab and not 'Runs'
df = pd.ExcelFile('/home/robert/Downloads/reg.xlsx').parse('Contacts')

# edit the data in pandas
df.rename(columns = {'Contact UUID':'contact_uuid'}, inplace = True)
df.rename(columns = {'URN':'urn'}, inplace = True)
df.rename(columns = {'Name':'name'}, inplace = True)
df.rename(columns = {'Groups':'groups'}, inplace = True)
df.rename(columns = {'SiteID':'siteid'}, inplace = True)
df.rename(columns = {'Type':'type'}, inplace = True)
df.rename(columns = {'First Seen':'first_seen'}, inplace = True)
df.rename(columns = {'Last Seen':'last_seen'}, inplace = True)
# Need to edit these date time variables to include Time Zone for Postgresql

df.rename(columns = {'Mail (Value) - IMAM Register':'mail'}, inplace = True)
# Mail (Value) - IMAM Register
df.rename(columns = {'Post_imp (Value) - IMAM Register':'post'}, inplace = True)
# Post_imp (Value) - IMAM Register

# Change the order (the index) of the columns
columnsTitles = ['contact_uuid','urn','name','groups','siteid','type','first_seen','last_seen','post','mail']
df2 = df.reindex(columns=columnsTitles)
df2.set_index('urn')

# do not share this on github
# engine = create_engine('postgresql://[user]:[pass]@[host]:[port]/[schema]')
engine = create_engine('postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**settings.DATABASES['default']))


try :
    df2.to_sql('registration', engine, schema='public', if_exists='replace')
    with engine.connect() as con:
        con.execute('ALTER TABLE registration ADD PRIMARY KEY (urn);')
        # add time zones with same code
except KeyboardInterrupt:
    print("load of registration data failed - db exists already")
# when using if_exists='replace' then all column names are deleted
# when using  if_exists='append' then all column names are maintained, but repeat migrations cause duplicates




# Create your models here.

# Registration
class Registration(models.Model):
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    groups = models.CharField(max_length=100)
    siteid = models.IntegerField()
    type = models.CharField(max_length=20)
    first_seen = models.DateTimeField()
    last_seen =  models.DateTimeField()
    post = models.CharField(max_length=30)
    mail = models.EmailField()

    # replaces reference home_registration
    class Meta:
        db_table = 'registration'
        managed =  False

    def __str__(self):
        return "Registration {}".format(self.name)



# Program data
class Program(models.Model):
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.IntegerField()
    name =   models.CharField(max_length=100)
    groups = models.CharField(max_length=100)
    # if supervisor enters the data than take SiteID from proSiteID
    siteid = models.IntegerField()
    first_seen = models.DateTimeField()
    last_seen =  models.DateTimeField()
    weeknum = models.IntegerField()
    role = models.CharField(max_length=20)
    # if supervisor enters the data then take Type from proType
    type = models.CharField(max_length=20)
    age_group = models.CharField(max_length=20)
    # Admissions and Exits
    # if data entry is from SC then don't forget to add
    beg =  models.IntegerField()
    amar = models.IntegerField()
    tin =  models.IntegerField()
    tout = models.IntegerField()
    dcur = models.IntegerField()
    dead = models.IntegerField()
    defu = models.IntegerField()
    dmed = models.IntegerField()
    confirm = models.CharField(max_length=20)


# Stock data
class Stock(models.Model):
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.IntegerField()
    name =   models.CharField(max_length=100)
    groups = models.CharField(max_length=100)
    # if supervisor enters the data than take SiteID from StoSiteID
    siteid = models.IntegerField()
    first_seen = models.DateTimeField()
    last_seen =  models.DateTimeField()
    # if supervisor enters the data then don't forget to take data
    # level (first, second, site)
    level = models.CharField(max_length=20)
    weeknum = models.IntegerField()
    # if supervisor enters the data then take Type from stoType
    type = models.CharField(max_length=20)
    rutf_in = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_used_carton = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_used_sachet = models.DecimalField(max_digits=7, decimal_places=2,)
    rutf_bal_cartons = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_bal_sachet =  models.DecimalField(max_digits=7, decimal_places=2,)
    f75_bal_carton =   models.DecimalField(max_digits=7, decimal_places=2,)
    f75_bal_sachet =   models.DecimalField(max_digits=7, decimal_places=2,)
    f100_bal_carton =  models.DecimalField(max_digits=7, decimal_places=2,)
    f100_bal_sachet =  models.DecimalField(max_digits=7, decimal_places=2,)
    confirm = models.CharField(max_length=20)


# State and LGA Stock data
class Lga(models.Model):
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.IntegerField()
    name =   models.CharField(max_length=100)
    groups = models.CharField(max_length=100)
    siteid = models.IntegerField()
    first_seen = models.DateTimeField('first seen')
    last_seen =  models.DateTimeField('last seen')
    weeknum = models.IntegerField()
    rutf_in =          models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_out_carton =  models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_bal_cartons = models.DecimalField(max_digits=8, decimal_places=2,)
    # can add tracking of f75 and f100 later at LGA level
    f75_bal_carton =   models.DecimalField(max_digits=7, decimal_places=2,)
    f100_bal_carton =  models.DecimalField(max_digits=7, decimal_places=2,)
    confirm = models.CharField(max_length=20)




# how do we load the raw data once and then start to use the api after ?
# this will be important as the database size increases

# def load_database:
#     Registration.contact_uuid = df.Contact_UUID