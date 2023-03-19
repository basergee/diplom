from django.contrib import admin

from .models import Handbook, Vehicle, Maintenance, Reclamation

admin.site.register([Handbook, Vehicle, Maintenance, Reclamation])
