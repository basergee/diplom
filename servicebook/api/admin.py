from django.contrib import admin

from .models import Handbook, Vehicle, Maintenance, Reclamation

# Register your models here.
admin.site.register([Handbook, Vehicle, Maintenance, Reclamation])
