from django.contrib import admin
from .models import City, Venue, Slot

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class SlotInline(admin.TabularInline):
    model = Slot
    extra = 1

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    list_filter = ('city',)
    search_fields = ('name', 'address')
    inlines = [SlotInline]

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('venue', 'resource_type', 'date', 'start_time', 'end_time', 'price', 'is_available')
    list_filter = ('venue__city', 'date', 'is_available', 'venue', 'resource_type')

