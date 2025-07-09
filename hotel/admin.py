from django.contrib import admin
from .models import Customer, RoomType, Room, Reservation, Payment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'nationality', 'created_at')
    list_filter = ('nationality', 'id_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'capacity', 'created_at')
    list_filter = ('capacity', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'floor', 'status', 'is_active')
    list_filter = ('room_type', 'floor', 'status', 'is_active')
    search_fields = ('number', 'notes')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_number', 'customer', 'room', 'check_in_date', 'check_out_date', 'status', 'total_amount')
    list_filter = ('status', 'check_in_date', 'check_out_date', 'created_at')
    search_fields = ('reservation_number', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('reservation__reservation_number', 'transaction_id')
    readonly_fields = ('id', 'created_at', 'updated_at')