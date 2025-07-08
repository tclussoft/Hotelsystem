from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class RestaurantArea(models.Model):
    """Restaurant areas/sections"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    """Restaurant table model"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Being Cleaned'),
        ('out_of_service', 'Out of Service')
    ]
    
    number = models.CharField(max_length=10, unique=True)
    area = models.ForeignKey(RestaurantArea, on_delete=models.CASCADE, related_name='tables')
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"Table {self.number} ({self.area.name})"

class MenuCategory(models.Model):
    """Menu categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Menu Categories"
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """Menu item model"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('out_of_stock', 'Out of Stock')
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], help_text="Cost to prepare this item")
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    calories = models.PositiveIntegerField(null=True, blank=True)
    allergens = models.TextField(blank=True, help_text="Comma-separated list of allergens")
    ingredients = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order(models.Model):
    """Restaurant order model"""
    ORDER_TYPES = [
        ('dine_in', 'Dine In'),
        ('takeaway', 'Takeaway'),
        ('room_service', 'Room Service'),
        ('delivery', 'Delivery')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=200, blank=True)
    room_number = models.CharField(max_length=10, blank=True)  # For room service
    delivery_address = models.TextField(blank=True)  # For delivery
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_instructions = models.TextField(blank=True)
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='served_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.get_order_type_display()}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            import random
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            suffix = str(random.randint(1000, 9999))
            self.order_number = f"ORD{prefix}{suffix}"
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        """Calculate order total"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.total_amount = self.subtotal + self.tax_amount + self.service_charge - self.discount_amount
        self.save()

class OrderItem(models.Model):
    """Individual items in an order"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled')
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class KitchenOrder(models.Model):
    """Kitchen order for preparation tracking"""
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served')
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='kitchen_order')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    estimated_completion = models.DateTimeField(null=True, blank=True)
    actual_completion = models.DateTimeField(null=True, blank=True)
    assigned_chef = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='kitchen_orders')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Kitchen Order {self.order.order_number} - {self.status}"

class Inventory(models.Model):
    """Restaurant inventory management"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
        ('bottles', 'Bottles'),
        ('cans', 'Cans'),
        ('boxes', 'Boxes')
    ]
    
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Inventory Items"
    
    def __str__(self):
        return f"{self.name} - {self.current_stock} {self.unit}"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    @property
    def stock_value(self):
        return self.current_stock * self.unit_cost

class StockMovement(models.Model):
    """Track inventory stock movements"""
    MOVEMENT_TYPES = [
        ('purchase', 'Purchase'),
        ('consumption', 'Consumption'),
        ('waste', 'Waste'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer')
    ]
    
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inventory_item.name} - {self.movement_type} - {self.quantity}"

class Bill(models.Model):
    """Restaurant billing"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('finalized', 'Finalized'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('room_charge', 'Room Charge'),
        ('digital_wallet', 'Digital Wallet')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_number = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10)  # Percentage
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10)  # Percentage
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    payment_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_bills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Bill {self.bill_number} - ${self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.bill_number:
            import datetime
            import random
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            suffix = str(random.randint(1000, 9999))
            self.bill_number = f"BILL{prefix}{suffix}"
        super().save(*args, **kwargs)
    
    def calculate_amounts(self):
        """Calculate all bill amounts"""
        self.subtotal = self.order.subtotal
        self.tax_amount = (self.subtotal * self.tax_rate) / 100
        self.service_charge = (self.subtotal * self.service_charge_rate) / 100
        self.discount_amount = (self.subtotal * self.discount_percentage) / 100
        self.total_amount = self.subtotal + self.tax_amount + self.service_charge - self.discount_amount
        self.save()

class TableReservation(models.Model):
    """Table reservation system"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation_number = models.CharField(max_length=20, unique=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    party_size = models.PositiveIntegerField()
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    duration_hours = models.PositiveIntegerField(default=2)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['reservation_date', 'reservation_time']
    
    def __str__(self):
        return f"Reservation {self.reservation_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            import datetime
            import random
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            suffix = str(random.randint(100, 999))
            self.reservation_number = f"RES{prefix}{suffix}"
        super().save(*args, **kwargs)