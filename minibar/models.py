from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from hotel.models import Room, Reservation
from decimal import Decimal
import uuid

class MinibarProduct(models.Model):
    """Minibar product catalog"""
    CATEGORY_CHOICES = [
        ('beverages', 'Beverages'),
        ('alcoholic', 'Alcoholic Drinks'),
        ('snacks', 'Snacks'),
        ('confectionery', 'Confectionery'),
        ('personal_care', 'Personal Care'),
        ('electronics', 'Electronics'),
        ('other', 'Other')
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    temperature_required = models.CharField(max_length=20, choices=[
        ('ambient', 'Ambient'),
        ('chilled', 'Chilled'),
        ('frozen', 'Frozen')
    ], default='ambient')
    expiry_days = models.PositiveIntegerField(help_text="Days until expiry")
    barcode = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Weight in grams")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - ${self.selling_price}"
    
    @property
    def profit_margin(self):
        return ((self.selling_price - self.unit_cost) / self.unit_cost * 100) if self.unit_cost > 0 else 0

class MinibarSetup(models.Model):
    """Minibar setup configuration for different room types"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class MinibarSetupItem(models.Model):
    """Items in a minibar setup"""
    setup = models.ForeignKey(MinibarSetup, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    position = models.CharField(max_length=20, blank=True, help_text="Position in minibar (e.g., shelf 1, slot A)")
    
    class Meta:
        unique_together = ['setup', 'product']
    
    def __str__(self):
        return f"{self.setup.name} - {self.quantity}x {self.product.name}"

class RoomMinibar(models.Model):
    """Minibar instance in a room"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('restocking', 'Being Restocked'),
        ('inspection', 'Under Inspection'),
        ('inactive', 'Inactive')
    ]
    
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='minibar')
    setup = models.ForeignKey(MinibarSetup, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_restocked = models.DateTimeField(null=True, blank=True)
    last_inspected = models.DateTimeField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Current temperature in Celsius")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Minibar - Room {self.room.number}"

class MinibarInventory(models.Model):
    """Current inventory of minibar items in rooms"""
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE)
    current_quantity = models.PositiveIntegerField(default=0)
    expected_quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['minibar', 'product']
    
    def __str__(self):
        return f"{self.minibar.room.number} - {self.product.name} ({self.current_quantity})"
    
    @property
    def is_missing(self):
        return self.current_quantity < self.expected_quantity

class MinibarConsumption(models.Model):
    """Track minibar consumption by guests"""
    STATUS_CHOICES = [
        ('detected', 'Detected'),
        ('confirmed', 'Confirmed'),
        ('billed', 'Billed'),
        ('disputed', 'Disputed'),
        ('refunded', 'Refunded')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='consumptions')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='minibar_consumptions')
    quantity_consumed = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    consumption_time = models.DateTimeField()
    detection_method = models.CharField(max_length=20, choices=[
        ('manual', 'Manual Check'),
        ('sensor', 'Sensor Detection'),
        ('guest_report', 'Guest Report')
    ], default='manual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='detected')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-consumption_time']
    
    def __str__(self):
        return f"Room {self.minibar.room.number} - {self.quantity_consumed}x {self.product.name}"
    
    def save(self, *args, **kwargs):
        self.total_amount = self.unit_price * self.quantity_consumed
        super().save(*args, **kwargs)

class RestockingOrder(models.Model):
    """Minibar restocking orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='restocking_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    scheduled_time = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='restocking_assignments')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_restocking_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Restocking {self.order_number} - Room {self.minibar.room.number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            import random
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            suffix = str(random.randint(100, 999))
            self.order_number = f"REST{prefix}{suffix}"
        super().save(*args, **kwargs)

class RestockingOrderItem(models.Model):
    """Items to be restocked in a restocking order"""
    order = models.ForeignKey(RestockingOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    quantity_supplied = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.quantity_requested}x {self.product.name}"

class MinibarInspection(models.Model):
    """Minibar inspection records"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    TYPE_CHOICES = [
        ('routine', 'Routine Inspection'),
        ('maintenance', 'Maintenance Check'),
        ('guest_complaint', 'Guest Complaint'),
        ('temperature_check', 'Temperature Check'),
        ('inventory_audit', 'Inventory Audit')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection_number = models.CharField(max_length=20, unique=True)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='inspections')
    inspection_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_date = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='minibar_inspections')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    temperature_reading = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    issues_found = models.TextField(blank=True)
    actions_taken = models.TextField(blank=True)
    next_inspection_due = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_inspections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"Inspection {self.inspection_number} - Room {self.minibar.room.number}"
    
    def save(self, *args, **kwargs):
        if not self.inspection_number:
            import datetime
            import random
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            suffix = str(random.randint(100, 999))
            self.inspection_number = f"INS{prefix}{suffix}"
        super().save(*args, **kwargs)

class MinibarAlert(models.Model):
    """Automated alerts for minibar issues"""
    ALERT_TYPES = [
        ('temperature', 'Temperature Alert'),
        ('low_stock', 'Low Stock'),
        ('consumption', 'High Consumption'),
        ('malfunction', 'Equipment Malfunction'),
        ('door_open', 'Door Left Open'),
        ('maintenance_due', 'Maintenance Due')
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('emergency', 'Emergency')
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed')
    ]
    
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    message = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Alert value (temperature, quantity, etc.)")
    threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Threshold that triggered the alert")
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - Room {self.minibar.room.number} - {self.severity}"