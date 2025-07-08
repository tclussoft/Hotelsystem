from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'room-types', views.RoomTypeViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'additional-charges', views.AdditionalChargeViewSet)
router.register(r'housekeeping-tasks', views.HousekeepingTaskViewSet)
router.register(r'maintenance-requests', views.MaintenanceRequestViewSet)

app_name = 'hotel_management'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Dashboard and reports
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/occupancy/', views.occupancy_report, name='occupancy_report'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/customer/', views.customer_report, name='customer_report'),
    
    # Quick actions
    path('quick-checkin/', views.quick_checkin, name='quick_checkin'),
    path('quick-checkout/', views.quick_checkout, name='quick_checkout'),
    path('room-status-update/', views.room_status_update, name='room_status_update'),
    
    # Reservation management
    path('reservations/create/', views.create_reservation, name='create_reservation'),
    path('reservations/<uuid:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<uuid:reservation_id>/checkin/', views.checkin_guest, name='checkin_guest'),
    path('reservations/<uuid:reservation_id>/checkout/', views.checkout_guest, name='checkout_guest'),
    path('reservations/<uuid:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # Payment processing
    path('payments/process/', views.process_payment, name='process_payment'),
    path('payments/<uuid:payment_id>/receipt/', views.payment_receipt, name='payment_receipt'),
    
    # Room management
    path('rooms/availability/', views.room_availability, name='room_availability'),
    path('rooms/calendar/', views.room_calendar, name='room_calendar'),
    
    # Customer management
    path('customers/search/', views.customer_search, name='customer_search'),
    path('customers/<uuid:customer_id>/history/', views.customer_history, name='customer_history'),
    
    # Housekeeping
    path('housekeeping/', views.housekeeping_dashboard, name='housekeeping_dashboard'),
    path('housekeeping/tasks/assign/', views.assign_housekeeping_task, name='assign_housekeeping_task'),
    
    # Maintenance
    path('maintenance/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('maintenance/requests/create/', views.create_maintenance_request, name='create_maintenance_request'),
    
    # AJAX endpoints
    path('ajax/room-availability/', views.ajax_room_availability, name='ajax_room_availability'),
    path('ajax/customer-search/', views.ajax_customer_search, name='ajax_customer_search'),
    path('ajax/reservation-summary/', views.ajax_reservation_summary, name='ajax_reservation_summary'),
]