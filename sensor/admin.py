from django.contrib import admin
from .models import Raspi, Sensor, Item

admin.site.register(Raspi)
admin.site.register(Sensor)
admin.site.register(Item)
