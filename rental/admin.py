from django.contrib import admin
from .models import Car
from .models import Booking

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_day', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','car','start_date','end_date','total_price')
    list_filter = ('start_date','end_date','car')
    search_fields = ('user__username','car__name')