from django.contrib import admin
from .models import Role, Profile, Booking, BookingDetail

# Register your models here.
admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(BookingDetail)
