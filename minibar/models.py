from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from hotel_management.models import Room, Reservation
from decimal import Decimal
import uuid

class MinibarProduct(models.Model):
    """Minibar product model"""
    PRODUCT_TYPE_CHOICES = [
        ('beverage', 'Beverage'),
        ('snack', 'Snack'),
        ('alcohol', 'Alcohol'),
        ('soft_drink', 'Soft Drink'),
        ('water', 'Water'),
        ('juice', 'Juice'),
        ('candy', 'Candy'),
        ('nuts', 'Nuts'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True)
    volume_size = models.CharField(max_length=50, blank=True, help_text="e.g., 330ml, 50g")
    calories = models.PositiveIntegerField(null=True, blank=True)
    alcohol_content = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        help_text="Alcohol percentage (e.g., 5.0 for 5%)"
    )
    allergen_info = models.TextField(blank=True)
    expiry_period_days = models.PositiveIntegerField(
        default=365,
        help_text="Number of days before expiry from purchase date"
    )
    supplier = models.CharField(max_length=200, blank=True)
    supplier_contact = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='minibar_products/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    requires_id_check = models.BooleanField(default=False, help_text="For alcoholic beverages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_type', 'name']

    def __str__(self):
        return f"{self.name} - ${self.price}"

    @property
    def profit_margin(self):
        if self.cost_price:
            return ((self.price - self.cost_price) / self.price) * 100
        return None

class MinibarSetup(models.Model):
    """Minibar setup configuration for different room types"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    room_types = models.ManyToManyField('hotel_management.RoomType', related_name='minibar_setups')
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MinibarSetupProduct(models.Model):
    """Products included in a minibar setup"""
    setup = models.ForeignKey(MinibarSetup, on_delete=models.CASCADE, related_name='setup_products')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE, related_name='setup_items')
    quantity = models.PositiveIntegerField(default=1)
    position = models.CharField(max_length=50, blank=True, help_text="Position in minibar (e.g., Shelf 1, Door)")
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['setup', 'product']
        ordering = ['position', 'product__name']

    def __str__(self):
        return f"{self.setup.name} - {self.product.name} x {self.quantity}"

class RoomMinibar(models.Model):
    """Individual room minibar instance"""
    MINIBAR_STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('restocking', 'Being Restocked'),
        ('out_of_order', 'Out of Order'),
        ('locked', 'Locked'),
    ]

    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='minibar')
    setup = models.ForeignKey(MinibarSetup, on_delete=models.SET_NULL, null=True, related_name='room_minibars')
    status = models.CharField(max_length=20, choices=MINIBAR_STATUS_CHOICES, default='active')
    last_restocked_date = models.DateTimeField(null=True, blank=True)
    last_checked_date = models.DateTimeField(null=True, blank=True)
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        help_text="Current temperature in Celsius"
    )
    is_locked = models.BooleanField(default=False)
    lock_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Minibar - Room {self.room.room_number}"

    @property
    def total_value(self):
        """Calculate total value of current inventory"""
        return sum(
            item.quantity * item.product.price 
            for item in self.current_inventory.all()
        )

    @property
    def needs_restocking(self):
        """Check if minibar needs restocking"""
        if not self.setup:
            return False
        
        for setup_product in self.setup.setup_products.all():
            current_item = self.current_inventory.filter(product=setup_product.product).first()
            current_quantity = current_item.quantity if current_item else 0
            if current_quantity < setup_product.quantity:
                return True
        return False

class MinibarInventory(models.Model):
    """Current inventory of products in a room minibar"""
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='current_inventory')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE, related_name='minibar_inventory')
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['minibar', 'product']
        ordering = ['product__name']

    def __str__(self):
        return f"{self.minibar.room.room_number} - {self.product.name} x {self.quantity}"

    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False

    @property
    def days_until_expiry(self):
        if self.expiry_date:
            return (self.expiry_date - timezone.now().date()).days
        return None

class MinibarConsumption(models.Model):
    """Track minibar product consumption"""
    CONSUMPTION_STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    consumption_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='consumptions')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='minibar_consumptions')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE, related_name='consumptions')
    quantity_consumed = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    consumption_time = models.DateTimeField(default=timezone.now)
    detected_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CONSUMPTION_STATUS_CHOICES, default='pending')
    detection_method = models.CharField(max_length=50, choices=[
        ('manual', 'Manual Entry'),
        ('sensor', 'Sensor Detection'),
        ('rfid', 'RFID Tracking'),
        ('checkout', 'Checkout Inspection'),
    ], default='manual')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_consumptions')
    confirmation_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_charged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-consumption_time']

    def __str__(self):
        return f"{self.reservation.customer.full_name} - {self.product.name} x {self.quantity_consumed}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        self.total_amount = self.unit_price * self.quantity_consumed
        super().save(*args, **kwargs)

class MinibarRestocking(models.Model):
    """Track minibar restocking activities"""
    RESTOCKING_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    restocking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='restocking_records')
    scheduled_date = models.DateTimeField()
    started_time = models.DateTimeField(null=True, blank=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RESTOCKING_STATUS_CHOICES, default='scheduled')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_restocking')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_restocking')
    notes = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_restocking')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Restocking - Room {self.minibar.room.room_number} - {self.scheduled_date.date()}"

class MinibarRestockingItem(models.Model):
    """Items added during restocking"""
    restocking = models.ForeignKey(MinibarRestocking, on_delete=models.CASCADE, related_name='restocking_items')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE, related_name='restocking_items')
    quantity_added = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restocking.restocking_id} - {self.product.name} x {self.quantity_added}"

    def save(self, *args, **kwargs):
        if not self.unit_cost:
            self.unit_cost = self.product.cost_price or self.product.price
        self.total_cost = self.unit_cost * self.quantity_added
        super().save(*args, **kwargs)

class MinibarInspection(models.Model):
    """Regular minibar inspections"""
    INSPECTION_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    INSPECTION_TYPE_CHOICES = [
        ('routine', 'Routine Inspection'),
        ('checkout', 'Checkout Inspection'),
        ('maintenance', 'Maintenance Inspection'),
        ('complaint', 'Complaint Investigation'),
    ]

    inspection_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    minibar = models.ForeignKey(RoomMinibar, on_delete=models.CASCADE, related_name='inspections')
    inspection_type = models.CharField(max_length=20, choices=INSPECTION_TYPE_CHOICES, default='routine')
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=INSPECTION_STATUS_CHOICES, default='scheduled')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='minibar_inspections')
    temperature_reading = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    cleanliness_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True,
        help_text="Rating from 1 (poor) to 5 (excellent)"
    )
    issues_found = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    photos = models.ImageField(upload_to='minibar_inspections/', null=True, blank=True)
    requires_maintenance = models.BooleanField(default=False)
    requires_restocking = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Inspection - Room {self.minibar.room.room_number} - {self.inspection_type}"

class MinibarInspectionItem(models.Model):
    """Items checked during inspection"""
    inspection = models.ForeignKey(MinibarInspection, on_delete=models.CASCADE, related_name='inspection_items')
    product = models.ForeignKey(MinibarProduct, on_delete=models.CASCADE, related_name='inspection_items')
    expected_quantity = models.PositiveIntegerField()
    actual_quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=20, choices=[
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('expired', 'Expired'),
        ('damaged', 'Damaged'),
    ], default='good')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inspection.inspection_id} - {self.product.name}"

    @property
    def variance(self):
        return self.actual_quantity - self.expected_quantity

class MinibarBilling(models.Model):
    """Billing summary for minibar charges"""
    BILLING_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('finalized', 'Finalized'),
        ('charged', 'Charged to Room'),
        ('paid', 'Paid'),
        ('disputed', 'Disputed'),
    ]

    billing_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='minibar_billings')
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=BILLING_STATUS_CHOICES, default='draft')
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    finalized_date = models.DateTimeField(null=True, blank=True)
    charged_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_date']

    def __str__(self):
        return f"Minibar Bill - {self.reservation.customer.full_name} - ${self.total_amount}"

    def calculate_totals(self):
        """Calculate billing totals from consumption records"""
        consumptions = MinibarConsumption.objects.filter(
            reservation=self.reservation,
            status='confirmed',
            consumption_time__range=[self.billing_period_start, self.billing_period_end]
        )
        
        self.subtotal = sum(c.total_amount for c in consumptions)
        self.tax_amount = self.subtotal * Decimal('0.10')  # 10% tax
        self.total_amount = self.subtotal + self.tax_amount
        return self.total_amount

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)

class MinibarSettings(models.Model):
    """Global minibar system settings"""
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=4, default=Decimal('0.1000'),
        help_text="Tax rate as decimal (e.g., 0.1000 for 10%)"
    )
    default_detection_delay = models.PositiveIntegerField(
        default=30,
        help_text="Minutes to wait before marking consumption as confirmed"
    )
    auto_charge_on_checkout = models.BooleanField(
        default=True,
        help_text="Automatically charge minibar consumption on checkout"
    )
    require_guest_confirmation = models.BooleanField(
        default=True,
        help_text="Require guest confirmation for charges above threshold"
    )
    confirmation_threshold = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal('50.00'),
        help_text="Amount above which guest confirmation is required"
    )
    inspection_frequency_days = models.PositiveIntegerField(
        default=7,
        help_text="How often to inspect minibars (in days)"
    )
    restocking_threshold_percentage = models.PositiveIntegerField(
        default=50,
        help_text="Restock when inventory falls below this percentage"
    )
    temperature_min = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal('2.0'),
        help_text="Minimum acceptable temperature in Celsius"
    )
    temperature_max = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal('8.0'),
        help_text="Maximum acceptable temperature in Celsius"
    )
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Minibar Settings"
        verbose_name_plural = "Minibar Settings"

    def __str__(self):
        return "Minibar System Settings"
