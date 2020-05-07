from django.contrib import admin

from .models import Model, Loaner, Record

# Register your models here.
admin.site.register(Model)
admin.site.register(Loaner)
admin.site.register(Record)
