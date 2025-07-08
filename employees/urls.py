from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'positions', views.PositionViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'salaries', views.SalaryViewSet)
router.register(r'payrolls', views.PayrollViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'leave-types', views.LeaveTypeViewSet)
router.register(r'leave-requests', views.LeaveRequestViewSet)
router.register(r'performance-reviews', views.PerformanceReviewViewSet)
router.register(r'training-programs', views.TrainingProgramViewSet)
router.register(r'training-enrollments', views.TrainingEnrollmentViewSet)

app_name = 'employees'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Employee dashboard
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    path('profile/', views.employee_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Attendance management
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/checkin/', views.checkin, name='checkin'),
    path('attendance/checkout/', views.checkout, name='checkout'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('attendance/calendar/', views.attendance_calendar, name='attendance_calendar'),
    
    # Leave management
    path('leaves/', views.leave_requests_view, name='leaves'),
    path('leaves/request/', views.create_leave_request, name='create_leave_request'),
    path('leaves/<int:request_id>/', views.leave_request_detail, name='leave_request_detail'),
    path('leaves/<int:request_id>/approve/', views.approve_leave_request, name='approve_leave_request'),
    path('leaves/<int:request_id>/reject/', views.reject_leave_request, name='reject_leave_request'),
    path('leaves/calendar/', views.leave_calendar, name='leave_calendar'),
    
    # Payroll management
    path('payroll/', views.payroll_view, name='payroll'),
    path('payroll/process/', views.process_payroll, name='process_payroll'),
    path('payroll/<int:payroll_id>/', views.payroll_detail, name='payroll_detail'),
    path('payroll/<int:payroll_id>/slip/', views.payroll_slip, name='payroll_slip'),
    path('payroll/reports/', views.payroll_reports, name='payroll_reports'),
    
    # Performance management
    path('performance/', views.performance_view, name='performance'),
    path('performance/reviews/', views.performance_reviews, name='performance_reviews'),
    path('performance/reviews/create/', views.create_performance_review, name='create_performance_review'),
    path('performance/reviews/<int:review_id>/', views.performance_review_detail, name='performance_review_detail'),
    
    # Training management
    path('training/', views.training_view, name='training'),
    path('training/programs/', views.training_programs, name='training_programs'),
    path('training/programs/<int:program_id>/', views.training_program_detail, name='training_program_detail'),
    path('training/enroll/<int:program_id>/', views.enroll_training, name='enroll_training'),
    path('training/my-enrollments/', views.my_training_enrollments, name='my_training_enrollments'),
    
    # Department management
    path('departments/', views.departments_view, name='departments'),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
    path('departments/<int:dept_id>/employees/', views.department_employees, name='department_employees'),
    
    # Reports
    path('reports/', views.employee_reports, name='reports'),
    path('reports/attendance/', views.attendance_reports, name='attendance_reports'),
    path('reports/payroll-summary/', views.payroll_summary_report, name='payroll_summary_report'),
    path('reports/employee-performance/', views.employee_performance_report, name='employee_performance_report'),
    
    # HR management
    path('hr/', views.hr_dashboard, name='hr_dashboard'),
    path('hr/employees/create/', views.create_employee, name='create_employee'),
    path('hr/employees/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('hr/salary/update/', views.update_salary, name='update_salary'),
    
    # AJAX endpoints
    path('ajax/employee-search/', views.ajax_employee_search, name='ajax_employee_search'),
    path('ajax/attendance-summary/', views.ajax_attendance_summary, name='ajax_attendance_summary'),
    path('ajax/department-stats/', views.ajax_department_stats, name='ajax_department_stats'),
]