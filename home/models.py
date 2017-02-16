from __future__ import unicode_literals

from django.db import models


# Load of initial data done with django custom commands
# use - python manage.py load_data


# Registration
class Registration(models.Model):
    index = models.BigIntegerField(primary_key=True)
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
        # if managed = False then will not rename following Django conventions
        managed = False

    def __str__(self):
        return "Registration {}".format(self.name)


# Program data
class Program(models.Model):
    index = models.BigIntegerField(primary_key=True)
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

    class Meta:
        db_table = 'program'
        managed = False
        unique_together = (('urn', 'first_seen'),)


    def __str__(self):
        return "Program {}".format(self.name)


# Stock data
class Stock(models.Model):
    index = models.BigIntegerField(primary_key=True)
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.IntegerField(primary_key=True)
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
    rutf_bal_carton = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_bal_sachet =  models.DecimalField(max_digits=7, decimal_places=2,)
    f75_bal_carton =   models.DecimalField(max_digits=7, decimal_places=2,)
    f75_bal_sachet =   models.DecimalField(max_digits=7, decimal_places=2,)
    f100_bal_carton =  models.DecimalField(max_digits=7, decimal_places=2,)
    f100_bal_sachet =  models.DecimalField(max_digits=7, decimal_places=2,)
    confirm = models.CharField(max_length=20)

    class Meta:
        db_table = 'stock'
        managed = False

    def __str__(self):
        return "Stock {}".format(self.name)


# State and LGA Stock data
class Lga(models.Model):
    index = models.BigIntegerField(primary_key=True)
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
    rutf_out =  models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_bal = models.DecimalField(max_digits=8, decimal_places=2,)
    # can add tracking of f75 and f100 later at LGA level
    # f75_bal_carton =   models.DecimalField(max_digits=7, decimal_places=2,)
    # f100_bal_carton =  models.DecimalField(max_digits=7, decimal_places=2,)
    confirm = models.CharField(max_length=20)

    class Meta:
        db_table = 'lga'
        managed = False

    def __str__(self):
        return "Lga {}".format(self.name)


# Site IDs
class Siteid(models.Model):
    index = models.BigIntegerField(primary_key=True)
    siteid = models.BigIntegerField(primary_key=True)
    state = models.TextField(blank=True, null=True)
    state_num = models.TextField(blank=True, null=True)
    lga = models.TextField(blank=True, null=True)
    lga_num = models.TextField(blank=True, null=True)
    ward = models.TextField(blank=True, null=True)
    sitename = models.TextField(blank=True, null=True)
    x_lat = models.FloatField(blank=True, null=True)
    y_lat = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'siteids'
        managed = False

    def __unicode__(self):
        return u"Siteid {}".format(self.sitename)


# how do we load the raw data once and then start to use the api after ?
# this will be important as the database size increases
