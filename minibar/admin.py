from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    MinibarProduct, MinibarSetup, MinibarSetupProduct, RoomMinibar,
    MinibarInventory, MinibarConsumption, MinibarRestocking, MinibarRestockingItem,
    MinibarInspection, MinibarInspectionItem, MinibarBilling, MinibarSettings
)

@admin.register(MinibarProduct)
class MinibarProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'product_type', 'price', 'cost_price', 'profit_margin', 'requires_id_check', 'is_active']
    list_filter = ['product_type', 'requires_id_check', 'is_active', 'created_at']
    search_fields = ['name', 'brand', 'barcode', 'description']
    readonly_fields = ['profit_margin', 'created_at', 'updated_at']
    list_editable = ['price', 'is_active']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'brand', 'product_type', 'description', 'barcode')
        }),
        ('Pricing', {
            'fields': ('price', 'cost_price', 'profit_margin')
        }),
        ('Details', {
            'fields': ('volume_size', 'calories', 'alcohol_content', 'allergen_info')
        }),
        ('Inventory', {
            'fields': ('expiry_period_days', 'supplier', 'supplier_contact')
        }),
        ('Status & Settings', {
            'fields': ('is_active', 'requires_id_check')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        })
    )

class MinibarSetupProductInline(admin.TabularInline):
    model = MinibarSetupProduct
    extra = 0
    fields = ['product', 'quantity', 'position', 'is_mandatory']

@admin.register(MinibarSetup)
class MinibarSetupAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_types_list', 'product_count', 'is_default', 'is_active', 'created_at']
    list_filter = ['is_default', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MinibarSetupProductInline]
    filter_horizontal = ['room_types']
    
    def room_types_list(self, obj):
        return ', '.join([rt.name for rt in obj.room_types.all()[:3]]) + ('...' if obj.room_types.count() > 3 else '')
    room_types_list.short_description = 'Room Types'
    
    def product_count(self, obj):
        return obj.setup_products.count()
    product_count.short_description = 'Products'

@admin.register(MinibarSetupProduct)
class MinibarSetupProductAdmin(admin.ModelAdmin):
    list_display = ['setup', 'product', 'quantity', 'position', 'is_mandatory']
    list_filter = ['is_mandatory', 'setup', 'product__product_type']
    search_fields = ['setup__name', 'product__name', 'position']

class MinibarInventoryInline(admin.TabularInline):
    model = MinibarInventory
    extra = 0
    readonly_fields = ['last_updated']
    fields = ['product', 'quantity', 'expiry_date', 'batch_number', 'last_updated']

@admin.register(RoomMinibar)
class RoomMinibarAdmin(admin.ModelAdmin):
    list_display = ['room', 'setup', 'status', 'total_value', 'needs_restocking', 'temperature', 'last_restocked_date']
    list_filter = ['status', 'setup', 'is_locked', 'last_restocked_date']
    search_fields = ['room__room_number', 'setup__name', 'notes']
    readonly_fields = ['total_value', 'needs_restocking', 'created_at', 'updated_at']
    inlines = [MinibarInventoryInline]
    list_editable = ['status']
    
    fieldsets = (
        ('Room & Setup', {
            'fields': ('room', 'setup', 'status')
        }),
        ('Monitoring', {
            'fields': ('temperature', 'last_restocked_date', 'last_checked_date')
        }),
        ('Security', {
            'fields': ('is_locked', 'lock_code')
        }),
        ('Status', {
            'fields': ('total_value', 'needs_restocking', 'notes')
        })
    )

@admin.register(MinibarInventory)
class MinibarInventoryAdmin(admin.ModelAdmin):
    list_display = ['minibar_room', 'product', 'quantity', 'expiry_date', 'is_expired', 'days_until_expiry', 'updated_by']
    list_filter = ['product__product_type', 'expiry_date', 'last_updated']
    search_fields = ['minibar__room__room_number', 'product__name', 'batch_number']
    readonly_fields = ['is_expired', 'days_until_expiry', 'last_updated']
    
    def minibar_room(self, obj):
        return obj.minibar.room.room_number
    minibar_room.short_description = 'Room'

@admin.register(MinibarConsumption)
class MinibarConsumptionAdmin(admin.ModelAdmin):
    list_display = ['consumption_id_short', 'reservation_link', 'product', 'quantity_consumed', 'total_amount', 'status', 'consumption_time']
    list_filter = ['status', 'detection_method', 'consumption_time', 'product__product_type']
    search_fields = ['consumption_id', 'reservation__customer__first_name', 'reservation__customer__last_name', 'product__name']
    readonly_fields = ['consumption_id', 'total_amount', 'detected_time', 'created_at', 'updated_at']
    date_hierarchy = 'consumption_time'
    list_editable = ['status']
    
    fieldsets = (
        ('Consumption Details', {
            'fields': ('consumption_id', 'minibar', 'reservation', 'product')
        }),
        ('Quantity & Amount', {
            'fields': ('quantity_consumed', 'unit_price', 'total_amount')
        }),
        ('Detection', {
            'fields': ('consumption_time', 'detected_time', 'detection_method')
        }),
        ('Status & Confirmation', {
            'fields': ('status', 'confirmed_by', 'confirmation_time', 'is_charged')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )
    
    def consumption_id_short(self, obj):
        return str(obj.consumption_id)[:8] + '...'
    consumption_id_short.short_description = 'Consumption ID'
    
    def reservation_link(self, obj):
        url = reverse('admin:hotel_management_reservation_change', args=[obj.reservation.pk])
        return format_html('<a href="{}">{}</a>', url, obj.reservation.customer.full_name)
    reservation_link.short_description = 'Reservation'

class MinibarRestockingItemInline(admin.TabularInline):
    model = MinibarRestockingItem
    extra = 0
    readonly_fields = ['total_cost']
    fields = ['product', 'quantity_added', 'unit_cost', 'total_cost', 'expiry_date', 'batch_number']

@admin.register(MinibarRestocking)
class MinibarRestockingAdmin(admin.ModelAdmin):
    list_display = ['restocking_id_short', 'minibar_room', 'scheduled_date', 'status', 'assigned_to', 'performed_by', 'total_cost']
    list_filter = ['status', 'scheduled_date', 'created_at']
    search_fields = ['restocking_id', 'minibar__room__room_number', 'assigned_to__username']
    readonly_fields = ['restocking_id', 'total_cost', 'created_at', 'updated_at']
    inlines = [MinibarRestockingItemInline]
    date_hierarchy = 'scheduled_date'
    
    def restocking_id_short(self, obj):
        return str(obj.restocking_id)[:8] + '...'
    restocking_id_short.short_description = 'Restocking ID'
    
    def minibar_room(self, obj):
        return obj.minibar.room.room_number
    minibar_room.short_description = 'Room'

@admin.register(MinibarRestockingItem)
class MinibarRestockingItemAdmin(admin.ModelAdmin):
    list_display = ['restocking_link', 'product', 'quantity_added', 'unit_cost', 'total_cost', 'expiry_date']
    list_filter = ['product__product_type', 'expiry_date', 'created_at']
    search_fields = ['restocking__restocking_id', 'product__name', 'batch_number']
    readonly_fields = ['total_cost', 'created_at']
    
    def restocking_link(self, obj):
        url = reverse('admin:minibar_minibarrestocking_change', args=[obj.restocking.pk])
        return format_html('<a href="{}">{}</a>', url, str(obj.restocking.restocking_id)[:8] + '...')
    restocking_link.short_description = 'Restocking'

class MinibarInspectionItemInline(admin.TabularInline):
    model = MinibarInspectionItem
    extra = 0
    readonly_fields = ['variance']
    fields = ['product', 'expected_quantity', 'actual_quantity', 'variance', 'condition', 'notes']

@admin.register(MinibarInspection)
class MinibarInspectionAdmin(admin.ModelAdmin):
    list_display = ['inspection_id_short', 'minibar_room', 'inspection_type', 'scheduled_date', 'status', 'inspector', 'cleanliness_rating']
    list_filter = ['inspection_type', 'status', 'scheduled_date', 'requires_maintenance', 'requires_restocking']
    search_fields = ['inspection_id', 'minibar__room__room_number', 'inspector__username']
    readonly_fields = ['inspection_id', 'created_at', 'updated_at']
    inlines = [MinibarInspectionItemInline]
    
    fieldsets = (
        ('Inspection Information', {
            'fields': ('inspection_id', 'minibar', 'inspection_type', 'inspector')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'completed_date', 'status')
        }),
        ('Findings', {
            'fields': ('temperature_reading', 'cleanliness_rating', 'issues_found', 'recommendations')
        }),
        ('Action Required', {
            'fields': ('requires_maintenance', 'requires_restocking')
        }),
        ('Media', {
            'fields': ('photos',),
            'classes': ('collapse',)
        })
    )
    
    def inspection_id_short(self, obj):
        return str(obj.inspection_id)[:8] + '...'
    inspection_id_short.short_description = 'Inspection ID'
    
    def minibar_room(self, obj):
        return obj.minibar.room.room_number
    minibar_room.short_description = 'Room'

@admin.register(MinibarInspectionItem)
class MinibarInspectionItemAdmin(admin.ModelAdmin):
    list_display = ['inspection_link', 'product', 'expected_quantity', 'actual_quantity', 'variance', 'condition']
    list_filter = ['condition', 'product__product_type', 'created_at']
    search_fields = ['inspection__inspection_id', 'product__name']
    readonly_fields = ['variance', 'created_at']
    
    def inspection_link(self, obj):
        url = reverse('admin:minibar_minibarinspection_change', args=[obj.inspection.pk])
        return format_html('<a href="{}">{}</a>', url, str(obj.inspection.inspection_id)[:8] + '...')
    inspection_link.short_description = 'Inspection'

@admin.register(MinibarBilling)
class MinibarBillingAdmin(admin.ModelAdmin):
    list_display = ['billing_id_short', 'reservation_link', 'billing_period_start', 'billing_period_end', 'total_amount', 'status']
    list_filter = ['status', 'generated_date', 'finalized_date']
    search_fields = ['billing_id', 'reservation__customer__first_name', 'reservation__customer__last_name']
    readonly_fields = ['billing_id', 'subtotal', 'tax_amount', 'total_amount', 'generated_date', 'created_at', 'updated_at']
    
    def billing_id_short(self, obj):
        return str(obj.billing_id)[:8] + '...'
    billing_id_short.short_description = 'Billing ID'
    
    def reservation_link(self, obj):
        url = reverse('admin:hotel_management_reservation_change', args=[obj.reservation.pk])
        return format_html('<a href="{}">{}</a>', url, obj.reservation.customer.full_name)
    reservation_link.short_description = 'Reservation'

@admin.register(MinibarSettings)
class MinibarSettingsAdmin(admin.ModelAdmin):
    list_display = ['tax_rate', 'auto_charge_on_checkout', 'require_guest_confirmation', 'confirmation_threshold']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance of settings
        return not MinibarSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False
