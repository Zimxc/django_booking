from django.contrib import admin

from booking.models import Booking, Room, Customer

# Register your models here.
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Room)