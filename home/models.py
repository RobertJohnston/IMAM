from __future__ import unicode_literals

from django.db import models


# Load of initial data done with django custom commands
# use - python manage.py load_data to load data from xls


class LastUpdatedAPICall(models.Model):
    kind = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u"%s: %s" % (self.kind, self.timestamp  )

# Import JSON data from API
class JsonRegistration(models.Model):
    uuid = models.CharField(editable=False, max_length=36, primary_key=True)
    json = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class JsonProgram(models.Model):
    id = models.BigIntegerField(primary_key=True)
    json = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class JsonStock(models.Model):
    id = models.BigIntegerField(primary_key=True)
    json = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class JsonWarehouse(models.Model):
    id = models.BigIntegerField(primary_key=True)
    json = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class RawRegistration(models.Model):
    uuid = models.CharField(editable=False, max_length=36, primary_key=True)
    urn = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=300)
    groups = models.CharField(max_length=1000, null=True, blank=True)
    siteid = models.CharField(max_length=300, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen =  models.DateTimeField(null=True, blank=True)
    post = models.CharField(max_length=30, null=True, blank=True)
    mail = models.CharField(max_length=60, null=True, blank=True)
    # Timestamps from our database
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


# Raw Program data
class RawProgram(models.Model):
    contact_uuid = models.TextField(blank=True, null=True)
    urn     = models.TextField()
    name    = models.TextField(blank=True, null=True)
    role    = models.TextField(blank=True, null=True)
    siteid  = models.TextField(blank=True, null=True)
    # From API
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField(blank=True, null=True)
    # Timestamps from our database
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    weeknum = models.TextField(blank=True, null=True)
    type    = models.TextField(blank=True, null=True)
    age_group = models.TextField(blank=True, null=True)
    # INPATIENTS and OUTPATIENTS
    beg   = models.TextField(blank=True, null=True)
    amar  = models.TextField(blank=True, null=True)
    tin   = models.TextField(blank=True, null=True)
    dcur  = models.TextField(blank=True, null=True)
    dead  = models.TextField(blank=True, null=True)
    defu  = models.TextField(blank=True, null=True)
    dmed  = models.TextField(blank=True, null=True)
    tout  = models.TextField(blank=True, null=True)
    confirm = models.TextField(blank=True, null=True)

    # state_num = models.TextField(blank=True, null=True)
    # lga_num   = models.TextField(blank=True, null=True)
    # year      = models.TextField(blank=True, null=True)

    # last_seen_weeknum = models.BigIntegerField(blank=True, null=True)
    # rep_year_wn = models.TextField(blank=True, null=True)
    # rep_weeknum = models.BigIntegerField(blank=True, null=True)
    # last_seen_dotw = models.BigIntegerField(blank=True, null=True)
    # last_seen_hour = models.BigIntegerField(blank=True, null=True)
    # year_weeknum = models.TextField(blank=True, null=True)
    # iso_rep_year_wn = models.TextField(blank=True, null=True)
    # iso_year_weeknum = models.TextField(blank=True, null=True)
    # iso_diff = models.BigIntegerField(blank=True, null=True)


class RawStock(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()

    rutf_in          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rutf_used_carton = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rutf_used_sachet = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rutf_bal_carton  = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rutf_bal_sachet  = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    f75_bal_carton   = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    f75_bal_sachet   = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    f100_bal_carton  = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    f100_bal_sachet  = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    state_num = models.BigIntegerField(blank=True, null=True)
    lga_num = models.BigIntegerField(blank=True, null=True)
    # Timestamps from our database
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)



# FIXME
class RawWarehouse(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    # Timestamps from our database
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)



# Registration
class Registration(models.Model):
    # index = models.BigIntegerField(primary_key=True)
    # contact_uuid = models.UUIDField(editable=False)
    contact_uuid = models.CharField(editable=False, max_length=36, primary_key=True)
    # Do not import URN as phone number field - leave in RapidPro format
    # urn = models.PhoneNumberField()
    urn = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=300)
    groups = models.CharField(max_length=1000, null=True, blank=True)
    siteid = models.BigIntegerField()
    type = models.CharField(max_length=20, null=True, blank=True)
    first_seen = models.DateTimeField()
    last_seen =  models.DateTimeField()
    post = models.CharField(max_length=30, null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    state_num = models.BigIntegerField(blank=True, null=True)
    lga_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'registration'
        # if managed = False then will not rename following Django conventions
        # managed = False

    def __unicode__(self): # Python 3: def __str__(self):
        return "Registration {}".format(self.name)


# Program data
class Program(models.Model):
    contact_uuid = models.TextField(blank=True, null=True)
    urn = models.TextField()
    name = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    siteid = models.BigIntegerField(blank=True, null=True)

    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField(blank=True, null=True)

    weeknum = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    age_group = models.TextField(blank=True, null=True)

    # Convert the inpatients and outpatients data into generic form
    beg = models.BigIntegerField(blank=True, null=True)
    amar = models.BigIntegerField(blank=True, null=True)
    tin = models.BigIntegerField(blank=True, null=True)
    dcur = models.BigIntegerField(blank=True, null=True)
    dead = models.BigIntegerField(blank=True, null=True)
    defu = models.BigIntegerField(blank=True, null=True)
    dmed = models.BigIntegerField(blank=True, null=True)
    tout = models.BigIntegerField(blank=True, null=True)
    confirm = models.TextField(blank=True, null=True)

    # Variables to accelerate analysis
    state_num = models.BigIntegerField(blank=True, null=True)
    lga_num = models.BigIntegerField(blank=True, null=True)

    year = models.BigIntegerField(blank=True, null=True)

    last_seen_weeknum = models.BigIntegerField(blank=True, null=True)
    rep_year_wn = models.TextField(blank=True, null=True)
    rep_weeknum = models.BigIntegerField(blank=True, null=True)
    last_seen_dotw = models.BigIntegerField(blank=True, null=True)
    last_seen_hour = models.BigIntegerField(blank=True, null=True)
    year_weeknum = models.TextField(blank=True, null=True)
    iso_rep_year_wn = models.TextField(blank=True, null=True)
    iso_year_weeknum = models.TextField(blank=True, null=True)
    iso_diff = models.BigIntegerField(blank=True, null=True)
    # since_x_weeks = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'program'
        unique_together = (('urn', 'first_seen'),)

    def __unicode__(self):
        return "Program {}".format(self.name)


# Stock data
class Stock(models.Model):
    # change index to id
    index = models.BigIntegerField(primary_key=True)
    contact_uuid = models.UUIDField(editable=False)
    urn = models.TextField()
    name = models.CharField(max_length=100)
    groups = models.CharField(max_length=100)

    # if supervisor enters the data then don't forget to take data
    # if supervisor enters the data than take SiteID from StoSiteID
    siteid = models.BigIntegerField()

    # if supervisor enters the data then take Type from stoType
    type = models.CharField(max_length=20)

    first_seen = models.DateTimeField()
    last_seen =  models.DateTimeField()

    # level (first, second, site)
    # level = models.CharField(max_length=20)
    weeknum = models.IntegerField()
    year = models.BigIntegerField()

    rutf_in          = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rutf_used_carton = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rutf_used_sachet = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    rutf_bal_carton  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rutf_bal_sachet  = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    f75_bal_carton   = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    f75_bal_sachet   = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    f100_bal_carton  = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    f100_bal_sachet  = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    state_num = models.BigIntegerField(blank=True, null=True)
    lga_num = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'stock'

    def __unicode__(self):
        return "Stock {}".format(self.name)


# Warehouse data  - State and LGA Stock data
class Warehouse(models.Model):
    index = models.BigIntegerField(primary_key=True)
    contact_uuid = models.UUIDField(editable=False)
    # problem to add phone number field to tools
    # urn = models.PhoneNumberField()
    urn = models.TextField()
    name = models.CharField(max_length=100)
    groups = models.CharField(max_length=100)
    siteid = models.BigIntegerField()
    first_seen = models.DateTimeField('first seen')
    last_seen =  models.DateTimeField('last seen')
    weeknum = models.IntegerField()
    year = models.BigIntegerField()
    rutf_in = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_out = models.DecimalField(max_digits=8, decimal_places=2,)
    rutf_bal = models.DecimalField(max_digits=8, decimal_places=2,)
    # can add tracking of f75 and f100 later at Warehouse level
    # f75_bal_carton =   models.DecimalField(max_digits=7, decimal_places=2,)
    # f100_bal_carton =  models.DecimalField(max_digits=7, decimal_places=2,)

    class Meta:
        db_table = 'warehouse'

    def __unicode__(self):
        return "Warehouse {}".format(self.name)


# First Admin IDs
class First_admin(models.Model):
    index = models.IntegerField()
    state = models.TextField(blank=True, null=True)
    state_num = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'first_admin'

    def __unicode__(self):
        return "First_admin {}".format(self.state)


# Second Admin IDs
class Second_admin(models.Model):
    index = models.BigIntegerField()
    state_num = models.ForeignKey(First_admin, db_column="state_num")
    lga = models.TextField(blank=True, null=True)
    lga_num = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'second_admin'

    def __unicode__(self):
        return "Second_admin {}".format(self.lga)


# Site IDs
class Site(models.Model):
    index = models.IntegerField()
    siteid = models.BigIntegerField(primary_key=True)
    sitename = models.TextField(blank=True, null=True)
    state_num = models.ForeignKey(First_admin, db_column="state_num")
    lga_num = models.ForeignKey(Second_admin, db_column="lga_num")
    ward = models.TextField(blank=True, null=True)
    x_long = models.IntegerField(blank=True, null=True)
    y_lat = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # add CLOSING DATE variable
    # closing_date = models.DateField(blank=True, null=True)
    # Site IDs are loaded in from excel. They are not taken from RapidPro, so they will not be rewritten regularly.

    class Meta:
        # This is reference of Django to Postgres
        db_table = 'site'
        managed = False

    def __unicode__(self):
        return "Site {}".format(self.sitename)

