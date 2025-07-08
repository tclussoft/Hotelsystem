from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

class Customer(models.Model):
    """Customer model for hotel guests"""
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, unique=True)
    id_type = models.CharField(max_length=50, choices=[
        ('passport', 'Passport'),
        ('national_id', 'National ID'),
        ('driver_license', 'Driver License'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class RoomType(models.Model):
    """Room type model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(help_text="List of amenities separated by commas")
    image = models.ImageField(upload_to='room_types/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_amenities_list(self):
        return [amenity.strip() for amenity in self.amenities.split(',') if amenity.strip()]

class Room(models.Model):
    """Room model"""
    ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('cleaning', 'Being Cleaned'),
        ('reserved', 'Reserved'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    floor = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['floor', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type.name}"

    @property
    def is_available(self):
        return self.status == 'available' and self.is_active

class Reservation(models.Model):
    """Reservation model"""
    RESERVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    reservation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    actual_check_in = models.DateTimeField(null=True, blank=True)
    actual_check_out = models.DateTimeField(null=True, blank=True)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    ], default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation {self.reservation_id} - {self.customer.full_name}"

    @property
    def duration_days(self):
        return (self.check_out_date - self.check_in_date).days

    @property
    def is_current(self):
        today = timezone.now().date()
        return self.check_in_date <= today <= self.check_out_date

    @property
    def is_overdue(self):
        today = timezone.now().date()
        return today > self.check_out_date and self.status == 'checked_in'

    def calculate_total_amount(self):
        """Calculate total amount based on room type and duration"""
        base_amount = self.room.room_type.base_price * self.duration_days
        return base_amount

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

class CheckInOut(models.Model):
    """Check-in and check-out tracking model"""
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='checkinout')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    check_in_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checkins')
    check_out_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checkouts')
    key_cards_issued = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Check-in/out for {self.reservation.customer.full_name}"

class Payment(models.Model):
    """Payment model for tracking payments"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('check', 'Check'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('reservation', 'Reservation Payment'),
        ('deposit', 'Deposit'),
        ('additional_charges', 'Additional Charges'),
        ('refund', 'Refund'),
    ]

    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    transaction_reference = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    is_refunded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount}"

class AdditionalCharge(models.Model):
    """Additional charges for reservations"""
    CHARGE_TYPE_CHOICES = [
        ('minibar', 'Minibar'),
        ('room_service', 'Room Service'),
        ('laundry', 'Laundry'),
        ('spa', 'Spa Services'),
        ('restaurant', 'Restaurant'),
        ('damage', 'Damage Charge'),
        ('late_checkout', 'Late Checkout'),
        ('extra_guest', 'Extra Guest'),
        ('other', 'Other'),
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='additional_charges')
    charge_type = models.CharField(max_length=20, choices=CHARGE_TYPE_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    charged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    charge_date = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.amount * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - ${self.total_amount}"

class HousekeepingTask(models.Model):
    """Housekeeping task management"""
    TASK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    TASK_TYPE_CHOICES = [
        ('cleaning', 'Room Cleaning'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Room Inspection'),
        ('deep_clean', 'Deep Cleaning'),
        ('amenity_restock', 'Amenity Restocking'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='housekeeping_tasks')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.task_type} - Room {self.room.room_number}"

class MaintenanceRequest(models.Model):
    """Maintenance request model"""
    REQUEST_STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='open')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_requests')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_requests')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_completion = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - Room {self.room.room_number}"
