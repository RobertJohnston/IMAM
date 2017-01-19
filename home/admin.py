from django.contrib import admin

from .models import Registration

# from .models import Registration, Program, Stock, Lga
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'urn', 'siteid', 'mail')

admin.site.register(Registration, RegistrationAdmin )
# admin.site.register(Program)
# admin.site.register(Stock)
# admin.site.register(Lga)
#

# Register your models here.
