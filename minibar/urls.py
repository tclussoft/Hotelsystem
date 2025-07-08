from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'products', views.MinibarProductViewSet)
router.register(r'setups', views.MinibarSetupViewSet)
router.register(r'room-minibars', views.RoomMinibarViewSet)
router.register(r'inventory', views.MinibarInventoryViewSet)
router.register(r'consumptions', views.MinibarConsumptionViewSet)
router.register(r'restocking', views.MinibarRestockingViewSet)
router.register(r'inspections', views.MinibarInspectionViewSet)
router.register(r'billing', views.MinibarBillingViewSet)

app_name = 'minibar'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Minibar dashboard
    path('dashboard/', views.minibar_dashboard, name='dashboard'),
    path('overview/', views.minibar_overview, name='overview'),
    
    # Product management
    path('products/', views.products_view, name='products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/disable/', views.disable_product, name='disable_product'),
    
    # Setup management
    path('setups/', views.setups_view, name='setups'),
    path('setups/create/', views.create_setup, name='create_setup'),
    path('setups/<int:setup_id>/', views.setup_detail, name='setup_detail'),
    path('setups/<int:setup_id>/edit/', views.edit_setup, name='edit_setup'),
    path('setups/<int:setup_id>/copy/', views.copy_setup, name='copy_setup'),
    
    # Room minibar management
    path('rooms/', views.room_minibars_view, name='room_minibars'),
    path('rooms/<int:minibar_id>/', views.room_minibar_detail, name='room_minibar_detail'),
    path('rooms/<int:minibar_id>/inventory/', views.minibar_inventory, name='minibar_inventory'),
    path('rooms/<int:minibar_id>/lock/', views.lock_minibar, name='lock_minibar'),
    path('rooms/<int:minibar_id>/unlock/', views.unlock_minibar, name='unlock_minibar'),
    path('rooms/<int:minibar_id>/temperature/', views.update_temperature, name='update_temperature'),
    
    # Consumption tracking
    path('consumptions/', views.consumptions_view, name='consumptions'),
    path('consumptions/record/', views.record_consumption, name='record_consumption'),
    path('consumptions/<uuid:consumption_id>/', views.consumption_detail, name='consumption_detail'),
    path('consumptions/<uuid:consumption_id>/confirm/', views.confirm_consumption, name='confirm_consumption'),
    path('consumptions/<uuid:consumption_id>/dispute/', views.dispute_consumption, name='dispute_consumption'),
    path('consumptions/<uuid:consumption_id>/refund/', views.refund_consumption, name='refund_consumption'),
    
    # Restocking operations
    path('restocking/', views.restocking_view, name='restocking'),
    path('restocking/schedule/', views.schedule_restocking, name='schedule_restocking'),
    path('restocking/<uuid:restocking_id>/', views.restocking_detail, name='restocking_detail'),
    path('restocking/<uuid:restocking_id>/start/', views.start_restocking, name='start_restocking'),
    path('restocking/<uuid:restocking_id>/complete/', views.complete_restocking, name='complete_restocking'),
    path('restocking/auto-schedule/', views.auto_schedule_restocking, name='auto_schedule_restocking'),
    
    # Inspection management
    path('inspections/', views.inspections_view, name='inspections'),
    path('inspections/schedule/', views.schedule_inspection, name='schedule_inspection'),
    path('inspections/<uuid:inspection_id>/', views.inspection_detail, name='inspection_detail'),
    path('inspections/<uuid:inspection_id>/perform/', views.perform_inspection, name='perform_inspection'),
    path('inspections/<uuid:inspection_id>/complete/', views.complete_inspection, name='complete_inspection'),
    
    # Billing and charges
    path('billing/', views.billing_view, name='billing'),
    path('billing/generate/', views.generate_billing, name='generate_billing'),
    path('billing/<uuid:billing_id>/', views.billing_detail, name='billing_detail'),
    path('billing/<uuid:billing_id>/finalize/', views.finalize_billing, name='finalize_billing'),
    path('billing/<uuid:billing_id>/charge/', views.charge_to_room, name='charge_to_room'),
    
    # Reports and analytics
    path('reports/', views.minibar_reports, name='reports'),
    path('reports/consumption/', views.consumption_report, name='consumption_report'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/inventory-turnover/', views.inventory_turnover_report, name='inventory_turnover_report'),
    path('reports/restocking/', views.restocking_report, name='restocking_report'),
    path('reports/temperature/', views.temperature_report, name='temperature_report'),
    
    # Maintenance and alerts
    path('maintenance/', views.maintenance_view, name='maintenance'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/low-stock/', views.low_stock_alerts, name='low_stock_alerts'),
    path('alerts/temperature/', views.temperature_alerts, name='temperature_alerts'),
    path('alerts/maintenance/', views.maintenance_alerts, name='maintenance_alerts'),
    
    # Settings
    path('settings/', views.minibar_settings, name='settings'),
    path('settings/update/', views.update_settings, name='update_settings'),
    path('settings/tax-rates/', views.tax_rate_settings, name='tax_rate_settings'),
    path('settings/temperature-limits/', views.temperature_limit_settings, name='temperature_limit_settings'),
    
    # Mobile app endpoints
    path('mobile/scan-consumption/', views.mobile_scan_consumption, name='mobile_scan_consumption'),
    path('mobile/restocking-checklist/', views.mobile_restocking_checklist, name='mobile_restocking_checklist'),
    path('mobile/inspection-form/', views.mobile_inspection_form, name='mobile_inspection_form'),
    
    # AJAX endpoints
    path('ajax/room-status/', views.ajax_room_status, name='ajax_room_status'),
    path('ajax/product-search/', views.ajax_product_search, name='ajax_product_search'),
    path('ajax/consumption-summary/', views.ajax_consumption_summary, name='ajax_consumption_summary'),
    path('ajax/restocking-needed/', views.ajax_restocking_needed, name='ajax_restocking_needed'),
    path('ajax/temperature-status/', views.ajax_temperature_status, name='ajax_temperature_status'),
]