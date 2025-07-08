from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    RestaurantArea, Table, MenuCategory, MenuItem, TableReservation,
    Order, OrderItem, Bill, Inventory, StockMovement, MenuItemInventory
)

@admin.register(RestaurantArea)
class RestaurantAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'table_count', 'is_smoking_allowed', 'is_outdoor', 'is_private', 'is_active']
    list_filter = ['is_smoking_allowed', 'is_outdoor', 'is_private', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def table_count(self, obj):
        return obj.tables.count()
    table_count.short_description = 'Tables'

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'area', 'capacity', 'status', 'is_active', 'updated_at']
    list_filter = ['area', 'status', 'capacity', 'is_active', 'created_at']
    search_fields = ['table_number', 'area__name', 'location_description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'is_active']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('area')

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu_items_count', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['display_order', 'is_active']
    
    def menu_items_count(self, obj):
        return obj.menu_items.count()
    menu_items_count.short_description = 'Menu Items'

class MenuItemInventoryInline(admin.TabularInline):
    model = MenuItemInventory
    extra = 0
    fields = ['inventory_item', 'quantity_required', 'is_optional']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'item_type', 'preparation_time', 'is_available', 'is_featured', 'display_order']
    list_filter = ['category', 'item_type', 'dietary_info', 'is_available', 'is_featured', 'is_chef_special']
    search_fields = ['name', 'description', 'ingredients']
    readonly_fields = ['profit_margin', 'created_at', 'updated_at']
    list_editable = ['price', 'is_available', 'is_featured', 'display_order']
    inlines = [MenuItemInventoryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'price', 'cost_price', 'profit_margin')
        }),
        ('Classification', {
            'fields': ('item_type', 'dietary_info', 'display_order')
        }),
        ('Details', {
            'fields': ('ingredients', 'allergen_info', 'preparation_time', 'calories', 'spice_level')
        }),
        ('Status', {
            'fields': ('is_available', 'is_featured', 'is_chef_special')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_id_short', 'customer_name', 'table', 'reservation_date', 'reservation_time', 'guest_count', 'status', 'created_by']
    list_filter = ['status', 'reservation_date', 'table__area', 'created_at']
    search_fields = ['reservation_id', 'customer_name', 'customer_phone', 'customer_email', 'table__table_number']
    readonly_fields = ['reservation_id', 'created_at', 'updated_at']
    date_hierarchy = 'reservation_date'
    list_editable = ['status']
    
    def reservation_id_short(self, obj):
        return str(obj.reservation_id)[:8] + '...'
    reservation_id_short.short_description = 'Reservation ID'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['menu_item', 'quantity', 'unit_price', 'total_price', 'special_instructions', 'status']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'guest_name_or_customer', 'table', 'order_type', 'status', 'total_amount', 'order_time']
    list_filter = ['order_type', 'status', 'order_time', 'table__area']
    search_fields = ['order_number', 'order_id', 'guest_name', 'customer__first_name', 'customer__last_name', 'room_number']
    readonly_fields = ['order_id', 'order_number', 'estimated_preparation_time', 'actual_preparation_time', 'created_at', 'updated_at']
    date_hierarchy = 'order_time'
    inlines = [OrderItemInline]
    list_editable = ['status']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'order_number', 'order_type', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer', 'guest_name', 'guest_phone', 'table', 'room_number', 'guest_count')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'service_charge', 'discount_amount', 'total_amount')
        }),
        ('Timing', {
            'fields': ('order_time', 'estimated_preparation_time', 'actual_preparation_time', 'ready_time', 'served_time', 'completed_time')
        }),
        ('Staff', {
            'fields': ('order_taken_by', 'prepared_by', 'served_by')
        }),
        ('Special Instructions', {
            'fields': ('special_instructions',),
            'classes': ('collapse',)
        })
    )
    
    def guest_name_or_customer(self, obj):
        return obj.guest_name or (obj.customer.full_name if obj.customer else 'N/A')
    guest_name_or_customer.short_description = 'Guest/Customer'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_link', 'menu_item', 'quantity', 'unit_price', 'total_price', 'status']
    list_filter = ['status', 'menu_item__category', 'order__order_type', 'created_at']
    search_fields = ['order__order_number', 'menu_item__name', 'special_instructions']
    readonly_fields = ['total_price', 'created_at']
    
    def order_link(self, obj):
        url = reverse('admin:restaurant_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_link.short_description = 'Order'

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'order_link', 'total_amount', 'payment_status', 'payment_method', 'generated_at', 'paid_at']
    list_filter = ['payment_status', 'payment_method', 'generated_at', 'paid_at']
    search_fields = ['bill_number', 'bill_id', 'order__order_number', 'transaction_reference']
    readonly_fields = ['bill_id', 'bill_number', 'balance_due', 'created_at', 'updated_at']
    date_hierarchy = 'generated_at'
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('bill_id', 'bill_number', 'order')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'service_charge', 'discount_amount', 'tip_amount', 'total_amount', 'amount_paid', 'balance_due')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_method', 'transaction_reference')
        }),
        ('Dates', {
            'fields': ('generated_at', 'paid_at')
        }),
        ('Staff & Notes', {
            'fields': ('generated_by', 'notes'),
            'classes': ('collapse',)
        })
    )
    
    def order_link(self, obj):
        url = reverse('admin:restaurant_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_link.short_description = 'Order'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'category', 'current_stock', 'unit', 'is_low_stock', 'unit_cost', 'stock_value', 'last_purchase_date', 'expiry_date']
    list_filter = ['category', 'unit', 'is_active', 'last_purchase_date', 'expiry_date']
    search_fields = ['item_name', 'supplier', 'storage_location']
    readonly_fields = ['is_low_stock', 'stock_value', 'created_at', 'updated_at']
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'movement_type', 'quantity', 'unit_cost', 'total_cost', 'movement_date', 'recorded_by']
    list_filter = ['movement_type', 'movement_date', 'created_at']
    search_fields = ['inventory_item__item_name', 'reference_number', 'notes']
    readonly_fields = ['total_cost', 'created_at']
    date_hierarchy = 'movement_date'

@admin.register(MenuItemInventory)
class MenuItemInventoryAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'inventory_item', 'quantity_required', 'is_optional', 'created_at']
    list_filter = ['is_optional', 'menu_item__category', 'inventory_item__category']
    search_fields = ['menu_item__name', 'inventory_item__item_name']
    readonly_fields = ['created_at']
