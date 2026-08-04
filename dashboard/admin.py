from django.contrib import admin
from .models import Business, Service, WorkingHour


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")


admin.site.register(Service)
admin.site.register(WorkingHour)