from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Department, Position, Employee, Salary, Payroll, Attendance,
    LeaveType, LeaveRequest, PerformanceReview, TrainingProgram, TrainingEnrollment
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_of_department', 'employee_count', 'budget', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'min_salary', 'max_salary', 'employee_count', 'is_active']
    list_filter = ['department', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'department__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'

class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0
    readonly_fields = ['total_salary', 'created_at']
    fields = ['base_salary', 'allowances', 'overtime_rate', 'effective_date', 'end_date', 'is_current']

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ['total_hours', 'created_at']
    fields = ['date', 'check_in_time', 'check_out_time', 'status', 'total_hours']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'position', 'employment_status', 'hire_date', 'years_of_service']
    list_filter = ['department', 'position', 'employment_status', 'employment_type', 'hire_date', 'gender']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email', 'phone_number', 'national_id']
    readonly_fields = ['created_at', 'updated_at', 'age', 'years_of_service']
    inlines = [SalaryInline]
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Employee Information', {
            'fields': ('employee_id', 'department', 'position', 'manager')
        }),
        ('Personal Details', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'age', 'gender', 'nationality', 'national_id')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Employment Details', {
            'fields': ('hire_date', 'years_of_service', 'employment_status', 'employment_type', 'termination_date', 'termination_reason')
        }),
        ('Work Information', {
            'fields': ('work_location', 'shift_type')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio', 'skills'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'department', 'position')

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'base_salary', 'allowances', 'total_salary', 'effective_date', 'is_current']
    list_filter = ['is_current', 'effective_date', 'created_at']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name']
    readonly_fields = ['total_salary', 'created_at', 'updated_at']
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'pay_period_start', 'pay_period_end', 'gross_salary', 'net_salary', 'status', 'payment_date']
    list_filter = ['status', 'payment_method', 'pay_period_start', 'payment_date']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name']
    readonly_fields = ['gross_salary', 'net_salary', 'created_at', 'updated_at']
    date_hierarchy = 'pay_period_start'
    
    fieldsets = (
        ('Employee & Period', {
            'fields': ('employee', 'pay_period_start', 'pay_period_end')
        }),
        ('Salary Components', {
            'fields': ('basic_salary', 'allowances', 'overtime_hours', 'overtime_amount', 'bonus')
        }),
        ('Deductions', {
            'fields': ('deductions', 'tax_deduction')
        }),
        ('Totals', {
            'fields': ('gross_salary', 'net_salary')
        }),
        ('Payment Information', {
            'fields': ('status', 'payment_date', 'payment_method', 'processed_by')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'date', 'check_in_time', 'check_out_time', 'total_hours', 'status']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name']
    readonly_fields = ['total_hours', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    list_editable = ['status']
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_days_per_year', 'is_paid', 'requires_approval', 'advance_notice_days', 'is_active']
    list_filter = ['is_paid', 'requires_approval', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'approved_by']
    list_filter = ['leave_type', 'status', 'start_date', 'approval_date']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name', 'reason']
    readonly_fields = ['total_days', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Leave Request', {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
        ('Supporting Documents', {
            'fields': ('supporting_document',),
            'classes': ('collapse',)
        })
    )
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'review_type', 'review_period_end', 'overall_rating', 'reviewer', 'is_final']
    list_filter = ['review_type', 'is_final', 'review_period_end']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name']
    readonly_fields = ['overall_rating', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('employee', 'review_period_start', 'review_period_end', 'review_type', 'reviewer')
        }),
        ('Performance Ratings', {
            'fields': ('job_knowledge', 'work_quality', 'productivity', 'communication', 'teamwork', 'leadership', 'punctuality', 'initiative', 'overall_rating')
        }),
        ('Comments', {
            'fields': ('strengths', 'areas_for_improvement', 'goals_for_next_period', 'additional_comments')
        }),
        ('Signatures', {
            'fields': ('is_final', 'employee_signature_date', 'reviewer_signature_date'),
            'classes': ('collapse',)
        })
    )
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'trainer', 'department', 'start_date', 'end_date', 'max_participants', 'enrolled_count', 'is_mandatory']
    list_filter = ['department', 'is_mandatory', 'certification_provided', 'start_date']
    search_fields = ['title', 'description', 'trainer']
    readonly_fields = ['created_at', 'updated_at']
    
    def enrolled_count(self, obj):
        return obj.enrollments.count()
    enrolled_count.short_description = 'Enrolled'

@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['employee_link', 'training_program', 'status', 'enrollment_date', 'completion_date', 'score', 'certificate_issued']
    list_filter = ['status', 'certificate_issued', 'enrollment_date', 'completion_date']
    search_fields = ['employee__employee_id', 'employee__user__first_name', 'employee__user__last_name', 'training_program__title']
    readonly_fields = ['enrollment_date']
    
    def employee_link(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.employee.pk])
        return format_html('<a href="{}">{}</a>', url, obj.employee.full_name)
    employee_link.short_description = 'Employee'
