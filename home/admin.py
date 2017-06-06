from django.contrib import admin

# from .models import Registration, Program, Stock, Lga
from .models import Registration, Program, Stock, Warehouse, First_admin, Second_admin, Site

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

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'urn', 'siteid', 'weeknum')
                    #'rutf_in', 'rutf_out', 'rutf_bal', 'confirm')
# First Admin
class First_adminAdmin(admin.ModelAdmin):
    list_display = ('state_num', 'state')

class Second_adminAdmin(admin.ModelAdmin):
    list_display = ('lga_num', 'lga', 'state_num')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('sitename', 'siteid', 'ward', 'x_long', 'y_lat', 'notes')
    # add opening date, closing date

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Warehouse, WarehouseAdmin)

admin.site.register(First_admin, First_adminAdmin)
admin.site.register(Second_admin, Second_adminAdmin)
admin.site.register(Site, SiteAdmin)

# admin.site.register(Siteid)
# add dbs for 1st and 2nd Admin?
