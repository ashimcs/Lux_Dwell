from django.contrib import admin
from .models import Property, Booking, Profile

admin.site.register(Property)
admin.site.register(Booking)
admin.site.register(Profile)