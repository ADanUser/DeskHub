from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slot', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    actions = ['confirm_bookings', 'reject_bookings', 'cancel_bookings']

    @admin.action(description='Подтвердить выбранные брони')
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Отклонить выбранные брони')
    def reject_bookings(self, request, queryset):
        queryset.update(status='rejected')
        for booking in queryset:
            booking.slot.is_available = True
            booking.slot.save()

    @admin.action(description='Отменить выбранные брони')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='canceled')
        for booking in queryset:
            booking.slot.is_available = True
            booking.slot.save()

