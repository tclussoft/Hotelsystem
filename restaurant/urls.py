from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'areas', views.RestaurantAreaViewSet)
router.register(r'tables', views.TableViewSet)
router.register(r'menu-categories', views.MenuCategoryViewSet)
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'table-reservations', views.TableReservationViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'bills', views.BillViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)

app_name = 'restaurant'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Restaurant dashboard
    path('dashboard/', views.restaurant_dashboard, name='dashboard'),
    path('pos/', views.pos_system, name='pos_system'),
    path('kitchen/', views.kitchen_display, name='kitchen_display'),
    
    # Table management
    path('tables/', views.table_management, name='table_management'),
    path('tables/<int:table_id>/', views.table_detail, name='table_detail'),
    path('tables/<int:table_id>/assign/', views.assign_table, name='assign_table'),
    path('tables/<int:table_id>/clean/', views.mark_table_clean, name='mark_table_clean'),
    path('table-layout/', views.table_layout, name='table_layout'),
    
    # Reservations
    path('reservations/', views.table_reservations, name='table_reservations'),
    path('reservations/create/', views.create_table_reservation, name='create_table_reservation'),
    path('reservations/<uuid:reservation_id>/', views.table_reservation_detail, name='table_reservation_detail'),
    path('reservations/<uuid:reservation_id>/confirm/', views.confirm_table_reservation, name='confirm_table_reservation'),
    path('reservations/<uuid:reservation_id>/cancel/', views.cancel_table_reservation, name='cancel_table_reservation'),
    
    # Menu management
    path('menu/', views.menu_view, name='menu'),
    path('menu/categories/', views.menu_categories, name='menu_categories'),
    path('menu/items/', views.menu_items, name='menu_items'),
    path('menu/items/create/', views.create_menu_item, name='create_menu_item'),
    path('menu/items/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('menu/items/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/print/', views.print_menu, name='print_menu'),
    
    # Order management
    path('orders/', views.orders_view, name='orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<uuid:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('orders/<uuid:order_id>/add-item/', views.add_order_item, name='add_order_item'),
    path('orders/<uuid:order_id>/bill/', views.generate_bill, name='generate_bill'),
    
    # Kitchen operations
    path('kitchen/orders/', views.kitchen_orders, name='kitchen_orders'),
    path('kitchen/orders/<int:item_id>/start/', views.start_cooking, name='start_cooking'),
    path('kitchen/orders/<int:item_id>/ready/', views.mark_ready, name='mark_ready'),
    path('kitchen/orders/<int:item_id>/served/', views.mark_served, name='mark_served'),
    
    # Billing and payments
    path('bills/', views.bills_view, name='bills'),
    path('bills/<uuid:bill_id>/', views.bill_detail, name='bill_detail'),
    path('bills/<uuid:bill_id>/payment/', views.process_bill_payment, name='process_bill_payment'),
    path('bills/<uuid:bill_id>/print/', views.print_bill, name='print_bill'),
    
    # Inventory management
    path('inventory/', views.inventory_view, name='inventory'),
    path('inventory/add-stock/', views.add_stock, name='add_stock'),
    path('inventory/adjust-stock/', views.adjust_stock, name='adjust_stock'),
    path('inventory/low-stock/', views.low_stock_items, name='low_stock_items'),
    path('inventory/movements/', views.stock_movements, name='stock_movements'),
    path('inventory/reports/', views.inventory_reports, name='inventory_reports'),
    
    # Reports
    path('reports/', views.restaurant_reports, name='reports'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/popular-items/', views.popular_items_report, name='popular_items_report'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/inventory-usage/', views.inventory_usage_report, name='inventory_usage_report'),
    
    # Room service
    path('room-service/', views.room_service_orders, name='room_service_orders'),
    path('room-service/create/', views.create_room_service_order, name='create_room_service_order'),
    path('room-service/<uuid:order_id>/deliver/', views.deliver_room_service, name='deliver_room_service'),
    
    # Customer features
    path('digital-menu/', views.digital_menu, name='digital_menu'),
    path('digital-menu/<int:table_id>/', views.table_digital_menu, name='table_digital_menu'),
    path('feedback/', views.customer_feedback, name='customer_feedback'),
    
    # AJAX endpoints
    path('ajax/table-status/', views.ajax_table_status, name='ajax_table_status'),
    path('ajax/menu-search/', views.ajax_menu_search, name='ajax_menu_search'),
    path('ajax/order-summary/', views.ajax_order_summary, name='ajax_order_summary'),
    path('ajax/kitchen-status/', views.ajax_kitchen_status, name='ajax_kitchen_status'),
    path('ajax/inventory-check/', views.ajax_inventory_check, name='ajax_inventory_check'),
]