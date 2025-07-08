from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from django.forms import TextInput, Textarea
from .models import (
    Customer, RoomType, Room, Reservation, CheckInOut, Payment,
    AdditionalCharge, HousekeepingTask, MaintenanceRequest
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'nationality', 'id_type', 'created_at']
    list_filter = ['nationality', 'id_type', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'id_number']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('customer_id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'nationality')
        }),
        ('Identification', {
            'fields': ('id_type', 'id_number')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'base_price', 'rooms_count', 'created_at']
    list_filter = ['capacity', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def rooms_count(self, obj):
        return obj.rooms.count()
    rooms_count.short_description = 'Number of Rooms'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'floor', 'status', 'is_active', 'updated_at']
    list_filter = ['room_type', 'floor', 'status', 'is_active', 'created_at']
    search_fields = ['room_number', 'room_type__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'is_active']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('room_type')

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['payment_id', 'created_at']
    fields = ['payment_type', 'amount', 'payment_method', 'transaction_reference', 'payment_date', 'processed_by']

class AdditionalChargeInline(admin.TabularInline):
    model = AdditionalCharge
    extra = 0
    readonly_fields = ['total_amount', 'created_at']
    fields = ['charge_type', 'description', 'amount', 'quantity', 'total_amount', 'is_paid']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_id_short', 'customer_link', 'room', 'check_in_date', 'check_out_date', 'status', 'payment_status', 'total_amount']
    list_filter = ['status', 'payment_status', 'check_in_date', 'check_out_date', 'created_at']
    search_fields = ['reservation_id', 'customer__first_name', 'customer__last_name', 'customer__email', 'room__room_number']
    readonly_fields = ['reservation_id', 'duration_days', 'is_current', 'is_overdue', 'created_at', 'updated_at']
    date_hierarchy = 'check_in_date'
    inlines = [PaymentInline, AdditionalChargeInline]
    
    fieldsets = (
        ('Reservation Details', {
            'fields': ('reservation_id', 'customer', 'room', 'status', 'created_by')
        }),
        ('Dates & Duration', {
            'fields': ('check_in_date', 'check_out_date', 'actual_check_in', 'actual_check_out', 'duration_days')
        }),
        ('Guest Information', {
            'fields': ('adults', 'children', 'special_requests')
        }),
        ('Payment Information', {
            'fields': ('total_amount', 'deposit_amount', 'payment_status')
        }),
        ('Status Information', {
            'fields': ('is_current', 'is_overdue'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def reservation_id_short(self, obj):
        return str(obj.reservation_id)[:8] + '...'
    reservation_id_short.short_description = 'Reservation ID'
    
    def customer_link(self, obj):
        url = reverse('admin:hotel_management_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', url, obj.customer.full_name)
    customer_link.short_description = 'Customer'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'room', 'room__room_type')

@admin.register(CheckInOut)
class CheckInOutAdmin(admin.ModelAdmin):
    list_display = ['reservation_link', 'customer_name', 'room_number', 'check_in_time', 'check_out_time', 'check_in_staff', 'check_out_staff']
    list_filter = ['check_in_time', 'check_out_time', 'created_at']
    search_fields = ['reservation__customer__first_name', 'reservation__customer__last_name', 'reservation__room__room_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def reservation_link(self, obj):
        url = reverse('admin:hotel_management_reservation_change', args=[obj.reservation.pk])
        return format_html('<a href="{}">{}</a>', url, str(obj.reservation.reservation_id)[:8] + '...')
    reservation_link.short_description = 'Reservation'
    
    def customer_name(self, obj):
        return obj.reservation.customer.full_name
    customer_name.short_description = 'Customer'
    
    def room_number(self, obj):
        return obj.reservation.room.room_number
    room_number.short_description = 'Room'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id_short', 'reservation_link', 'amount', 'payment_method', 'payment_type', 'payment_date', 'processed_by']
    list_filter = ['payment_method', 'payment_type', 'payment_date', 'is_refunded']
    search_fields = ['payment_id', 'transaction_reference', 'reservation__customer__first_name', 'reservation__customer__last_name']
    readonly_fields = ['payment_id', 'created_at']
    date_hierarchy = 'payment_date'
    
    def payment_id_short(self, obj):
        return str(obj.payment_id)[:8] + '...'
    payment_id_short.short_description = 'Payment ID'
    
    def reservation_link(self, obj):
        url = reverse('admin:hotel_management_reservation_change', args=[obj.reservation.pk])
        return format_html('<a href="{}">{}</a>', url, str(obj.reservation.reservation_id)[:8] + '...')
    reservation_link.short_description = 'Reservation'

@admin.register(AdditionalCharge)
class AdditionalChargeAdmin(admin.ModelAdmin):
    list_display = ['reservation_link', 'charge_type', 'description', 'amount', 'quantity', 'total_amount', 'is_paid', 'charge_date']
    list_filter = ['charge_type', 'is_paid', 'charge_date']
    search_fields = ['description', 'reservation__customer__first_name', 'reservation__customer__last_name']
    readonly_fields = ['total_amount', 'created_at']
    list_editable = ['is_paid']
    
    def reservation_link(self, obj):
        url = reverse('admin:hotel_management_reservation_change', args=[obj.reservation.pk])
        return format_html('<a href="{}">{}</a>', url, str(obj.reservation.reservation_id)[:8] + '...')
    reservation_link.short_description = 'Reservation'

@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    list_display = ['room', 'task_type', 'priority', 'status', 'assigned_to', 'due_date', 'created_by']
    list_filter = ['task_type', 'priority', 'status', 'due_date', 'created_at']
    search_fields = ['room__room_number', 'description', 'assigned_to__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'assigned_to']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Task Information', {
            'fields': ('room', 'task_type', 'description', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Schedule', {
            'fields': ('due_date', 'started_at', 'completed_at')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['room', 'title', 'priority', 'status', 'reported_by', 'assigned_to', 'estimated_cost', 'created_at']
    list_filter = ['priority', 'status', 'created_at', 'estimated_completion']
    search_fields = ['room__room_number', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'assigned_to']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('room', 'title', 'description', 'priority')
        }),
        ('Assignment', {
            'fields': ('reported_by', 'assigned_to')
        }),
        ('Cost Estimation', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Timeline', {
            'fields': ('estimated_completion', 'completed_at')
        }),
        ('Status & Resolution', {
            'fields': ('status', 'resolution_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# Customize admin site header and title
admin.site.site_header = "Tclussoft Hotel Management System"
admin.site.site_title = "Tclussoft Hotel Admin"
admin.site.index_title = "Hotel Management Dashboard"
