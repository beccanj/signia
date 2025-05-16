from django.contrib import admin

from main.models import Person

# Register your models here.
admin.site.site_header = 'Signia'
admin.site.site_title = 'Manage your clients info!'


admin.site.register(Person)
