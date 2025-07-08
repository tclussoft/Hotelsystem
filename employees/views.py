from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Department, Position, Employee, Salary, Payroll, Attendance,
    LeaveType, LeaveRequest, PerformanceReview, TrainingProgram, TrainingEnrollment
)

# API ViewSets
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated]

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated]

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated]

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    permission_classes = [IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    permission_classes = [IsAuthenticated]

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    permission_classes = [IsAuthenticated]

class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.all()
    permission_classes = [IsAuthenticated]

class TrainingEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = TrainingEnrollment.objects.all()
    permission_classes = [IsAuthenticated]

# Placeholder Views
@login_required
def employee_dashboard(request):
    return HttpResponse("Employee Dashboard - Coming Soon")

@login_required
def employee_profile(request):
    return HttpResponse("Employee Profile - Coming Soon")

@login_required
def edit_profile(request):
    return HttpResponse("Edit Profile - Coming Soon")

@login_required
def attendance_view(request):
    return HttpResponse("Attendance - Coming Soon")

@login_required
def checkin(request):
    return HttpResponse("Check In - Coming Soon")

@login_required
def checkout(request):
    return HttpResponse("Check Out - Coming Soon")

@login_required
def attendance_report(request):
    return HttpResponse("Attendance Report - Coming Soon")

@login_required
def attendance_calendar(request):
    return HttpResponse("Attendance Calendar - Coming Soon")

@login_required
def leave_requests_view(request):
    return HttpResponse("Leave Requests - Coming Soon")

@login_required
def create_leave_request(request):
    return HttpResponse("Create Leave Request - Coming Soon")

@login_required
def leave_request_detail(request, request_id):
    return HttpResponse(f"Leave Request Detail {request_id} - Coming Soon")

@login_required
def approve_leave_request(request, request_id):
    return HttpResponse(f"Approve Leave Request {request_id} - Coming Soon")

@login_required
def reject_leave_request(request, request_id):
    return HttpResponse(f"Reject Leave Request {request_id} - Coming Soon")

@login_required
def leave_calendar(request):
    return HttpResponse("Leave Calendar - Coming Soon")

@login_required
def payroll_view(request):
    return HttpResponse("Payroll - Coming Soon")

@login_required
def process_payroll(request):
    return HttpResponse("Process Payroll - Coming Soon")

@login_required
def payroll_detail(request, payroll_id):
    return HttpResponse(f"Payroll Detail {payroll_id} - Coming Soon")

@login_required
def payroll_slip(request, payroll_id):
    return HttpResponse(f"Payroll Slip {payroll_id} - Coming Soon")

@login_required
def payroll_reports(request):
    return HttpResponse("Payroll Reports - Coming Soon")

@login_required
def performance_view(request):
    return HttpResponse("Performance - Coming Soon")

@login_required
def performance_reviews(request):
    return HttpResponse("Performance Reviews - Coming Soon")

@login_required
def create_performance_review(request):
    return HttpResponse("Create Performance Review - Coming Soon")

@login_required
def performance_review_detail(request, review_id):
    return HttpResponse(f"Performance Review Detail {review_id} - Coming Soon")

@login_required
def training_view(request):
    return HttpResponse("Training - Coming Soon")

@login_required
def training_programs(request):
    return HttpResponse("Training Programs - Coming Soon")

@login_required
def training_program_detail(request, program_id):
    return HttpResponse(f"Training Program Detail {program_id} - Coming Soon")

@login_required
def enroll_training(request, program_id):
    return HttpResponse(f"Enroll Training {program_id} - Coming Soon")

@login_required
def my_training_enrollments(request):
    return HttpResponse("My Training Enrollments - Coming Soon")

@login_required
def departments_view(request):
    return HttpResponse("Departments - Coming Soon")

@login_required
def department_detail(request, dept_id):
    return HttpResponse(f"Department Detail {dept_id} - Coming Soon")

@login_required
def department_employees(request, dept_id):
    return HttpResponse(f"Department Employees {dept_id} - Coming Soon")

@login_required
def employee_reports(request):
    return HttpResponse("Employee Reports - Coming Soon")

@login_required
def attendance_reports(request):
    return HttpResponse("Attendance Reports - Coming Soon")

@login_required
def payroll_summary_report(request):
    return HttpResponse("Payroll Summary Report - Coming Soon")

@login_required
def employee_performance_report(request):
    return HttpResponse("Employee Performance Report - Coming Soon")

@login_required
def hr_dashboard(request):
    return HttpResponse("HR Dashboard - Coming Soon")

@login_required
def create_employee(request):
    return HttpResponse("Create Employee - Coming Soon")

@login_required
def edit_employee(request, employee_id):
    return HttpResponse(f"Edit Employee {employee_id} - Coming Soon")

@login_required
def update_salary(request):
    return HttpResponse("Update Salary - Coming Soon")

# AJAX Views
@csrf_exempt
def ajax_employee_search(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Employee Search - Coming Soon'})

@csrf_exempt
def ajax_attendance_summary(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Attendance Summary - Coming Soon'})

@csrf_exempt
def ajax_department_stats(request):
    return JsonResponse({'status': 'success', 'message': 'AJAX Department Stats - Coming Soon'})
