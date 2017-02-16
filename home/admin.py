from django.contrib import admin

# from .models import Registration, Program, Stock, Lga
from .models import Registration, Program, Stock, Lga

class RegistrationAdmin(admin.ModelAdmin):
    # here am able to access the variables in Registration using their names (django ORM)
    list_display = ('name', 'urn', 'siteid', 'type', 'post', 'mail')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'urn', 'siteid', 'type', 'weeknum', 'beg', 'amar')

class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'urn', 'siteid', 'type', 'weeknum', 'rutf_in',
                    'rutf_used_carton', 'rutf_used_sachet')
                    # ERRORS in STOCK import
                    #'rutf_bal_carton', 'rutf_used_sachet',
                    #'f75_bal_carton', 'f75_bal_carton', 'f100_bal_carton', 'f100_bal_carton', 'confirm')

class LgaAdmin(admin.ModelAdmin):
    list_display = ('name', 'urn', 'siteid', 'weeknum')
                    #'rutf_in', 'rutf_out', 'rutf_bal', 'confirm')

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Lga, LgaAdmin)

# admin.site.register(Siteid)
# add dbs for 1st and 2nd Admin?
