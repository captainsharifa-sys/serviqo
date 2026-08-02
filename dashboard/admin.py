from django.contrib import admin
from .models import Business, Service, WorkingHour

admin.site.register(Business)
admin.site.register(Service)
admin.site.register(WorkingHour)