from django.contrib import admin
from .models import flight, passenger

# Register your models here.
admin.site.register(flight)
admin.site.register(passenger)