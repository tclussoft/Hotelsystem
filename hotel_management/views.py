from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Customer, RoomType, Room, Reservation, CheckInOut, Payment,
    AdditionalCharge, HousekeepingTask, MaintenanceRequest
)

# API ViewSets for REST Framework
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    permission_classes = [IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

class AdditionalChargeViewSet(viewsets.ModelViewSet):
    queryset = AdditionalCharge.objects.all()
    permission_classes = [IsAuthenticated]

class HousekeepingTaskViewSet(viewsets.ModelViewSet):
    queryset = HousekeepingTask.objects.all()
    permission_classes = [IsAuthenticated]

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    permission_classes = [IsAuthenticated]

# Regular Views
@login_required
def dashboard_view(request):
    return HttpResponse("Hotel Management Dashboard - Coming Soon")

@login_required
def reports_view(request):
    return HttpResponse("Reports - Coming Soon")

@login_required
def occupancy_report(request):
    return HttpResponse("Occupancy Report - Coming Soon")

@login_required
def revenue_report(request):
    return HttpResponse("Revenue Report - Coming Soon")

@login_required
def customer_report(request):
    return HttpResponse("Customer Report - Coming Soon")

@login_required
def quick_checkin(request):
    return HttpResponse("Quick Check-in - Coming Soon")

@login_required
def quick_checkout(request):
    return HttpResponse("Quick Check-out - Coming Soon")

@login_required
def room_status_update(request):
    return HttpResponse("Room Status Update - Coming Soon")

@login_required
def create_reservation(request):
    return HttpResponse("Create Reservation - Coming Soon")

@login_required
def reservation_detail(request, reservation_id):
    return HttpResponse(f"Reservation Detail {reservation_id} - Coming Soon")

@login_required
def checkin_guest(request, reservation_id):
    return HttpResponse(f"Check-in Guest {reservation_id} - Coming Soon")

@login_required
def checkout_guest(request, reservation_id):
    return HttpResponse(f"Check-out Guest {reservation_id} - Coming Soon")

@login_required
def cancel_reservation(request, reservation_id):
    return HttpResponse(f"Cancel Reservation {reservation_id} - Coming Soon")

@login_required
def process_payment(request):
    return HttpResponse("Process Payment - Coming Soon")

@login_required
def payment_receipt(request, payment_id):
    return HttpResponse(f"Payment Receipt {payment_id} - Coming Soon")

@login_required
def room_availability(request):
    return HttpResponse("Room Availability - Coming Soon")

@login_required
def room_calendar(request):
    return HttpResponse("Room Calendar - Coming Soon")

@login_required
def customer_search(request):
    return HttpResponse("Customer Search - Coming Soon")

@login_required
def customer_history(request, customer_id):
    return HttpResponse(f"Customer History {customer_id} - Coming Soon")

@login_required
def housekeeping_dashboard(request):
    return HttpResponse("Housekeeping Dashboard - Coming Soon")

@login_required
def assign_housekeeping_task(request):
    return HttpResponse("Assign Housekeeping Task - Coming Soon")

@login_required
def maintenance_dashboard(request):
    return HttpResponse("Maintenance Dashboard - Coming Soon")

@login_required
def create_maintenance_request(request):
    return HttpResponse("Create Maintenance Request - Coming Soon")

# AJAX Views
@csrf_exempt
def ajax_room_availability(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Room Availability - Coming Soon'})

@csrf_exempt
def ajax_customer_search(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Customer Search - Coming Soon'})

@csrf_exempt
def ajax_reservation_summary(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Reservation Summary - Coming Soon'})
