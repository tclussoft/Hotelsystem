from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

class Department(models.Model):
    """Department model for organizing employees"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    """Job position model"""
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.department.name}"

class Employee(models.Model):
    """Employee model extending Django User"""
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
        ('suspended', 'Suspended'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('intern', 'Intern'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='employees')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    # Personal Information
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    national_id = models.CharField(max_length=50, unique=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Employment Details
    hire_date = models.DateField()
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='active')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    
    # Work Details
    work_location = models.CharField(max_length=100, default='Main Hotel')
    shift_type = models.CharField(max_length=20, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
        ('rotating', 'Rotating'),
    ], default='morning')
    
    # Profile
    profile_picture = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="List of skills separated by commas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def years_of_service(self):
        today = timezone.now().date()
        return today.year - self.hire_date.year - ((today.month, today.day) < (self.hire_date.month, self.hire_date.day))

class Salary(models.Model):
    """Salary model for tracking employee compensation"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.employee.full_name} - ${self.total_salary}"

    @property
    def total_salary(self):
        return self.base_salary + self.allowances

class Payroll(models.Model):
    """Payroll model for monthly salary processing"""
    PAYROLL_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYROLL_STATUS_CHOICES, default='draft')
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    ], default='bank_transfer')
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payrolls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pay_period_start']
        unique_together = ['employee', 'pay_period_start', 'pay_period_end']

    def __str__(self):
        return f"{self.employee.full_name} - {self.pay_period_start.strftime('%B %Y')}"

    def calculate_gross_salary(self):
        self.gross_salary = self.basic_salary + self.allowances + self.overtime_amount + self.bonus
        return self.gross_salary

    def calculate_net_salary(self):
        self.net_salary = self.gross_salary - self.deductions - self.tax_deduction
        return self.net_salary

    def save(self, *args, **kwargs):
        self.calculate_gross_salary()
        self.calculate_net_salary()
        super().save(*args, **kwargs)

class Attendance(models.Model):
    """Daily attendance tracking"""
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default='present')
    notes = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_attendance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

    def calculate_total_hours(self):
        if self.check_in_time and self.check_out_time:
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            
            # Handle overnight shifts
            if check_out < check_in:
                check_out += timedelta(days=1)
            
            total_time = check_out - check_in
            
            # Subtract break time if available
            if self.break_start_time and self.break_end_time:
                break_start = datetime.combine(self.date, self.break_start_time)
                break_end = datetime.combine(self.date, self.break_end_time)
                break_duration = break_end - break_start
                total_time -= break_duration
            
            self.total_hours = round(total_time.total_seconds() / 3600, 2)
        return self.total_hours

    def save(self, *args, **kwargs):
        self.calculate_total_hours()
        super().save(*args, **kwargs)

class LeaveType(models.Model):
    """Leave type model"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    max_days_per_year = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    advance_notice_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    """Leave request model"""
    LEAVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    supporting_document = models.FileField(upload_to='leave_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name} ({self.start_date} to {self.end_date})"

    def calculate_total_days(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        self.total_days = self.calculate_total_days()
        super().save(*args, **kwargs)

class PerformanceReview(models.Model):
    """Performance review model"""
    REVIEW_TYPE_CHOICES = [
        ('annual', 'Annual Review'),
        ('quarterly', 'Quarterly Review'),
        ('probation', 'Probation Review'),
        ('promotion', 'Promotion Review'),
    ]

    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_reviews')
    
    # Performance Metrics
    job_knowledge = models.PositiveIntegerField(choices=RATING_CHOICES)
    work_quality = models.PositiveIntegerField(choices=RATING_CHOICES)
    productivity = models.PositiveIntegerField(choices=RATING_CHOICES)
    communication = models.PositiveIntegerField(choices=RATING_CHOICES)
    teamwork = models.PositiveIntegerField(choices=RATING_CHOICES)
    leadership = models.PositiveIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    punctuality = models.PositiveIntegerField(choices=RATING_CHOICES)
    initiative = models.PositiveIntegerField(choices=RATING_CHOICES)
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals_for_next_period = models.TextField()
    additional_comments = models.TextField(blank=True)
    
    is_final = models.BooleanField(default=False)
    employee_signature_date = models.DateTimeField(null=True, blank=True)
    reviewer_signature_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_period_end']

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_type} ({self.review_period_end})"

    def calculate_overall_rating(self):
        ratings = [
            self.job_knowledge,
            self.work_quality,
            self.productivity,
            self.communication,
            self.teamwork,
            self.punctuality,
            self.initiative,
        ]
        
        if self.leadership:
            ratings.append(self.leadership)
        
        self.overall_rating = sum(ratings) / len(ratings)
        return self.overall_rating

    def save(self, *args, **kwargs):
        self.calculate_overall_rating()
        super().save(*args, **kwargs)

class TrainingProgram(models.Model):
    """Training program model"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    max_participants = models.PositiveIntegerField()
    cost_per_participant = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_mandatory = models.BooleanField(default=False)
    certification_provided = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TrainingEnrollment(models.Model):
    """Training enrollment model"""
    ENROLLMENT_STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_enrollments')
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='enrolled')
    completion_date = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    certificate_issued = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ['employee', 'training_program']

    def __str__(self):
        return f"{self.employee.full_name} - {self.training_program.title}"
