from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from hotel_management.models import Customer, Reservation
import uuid

class RestaurantArea(models.Model):
    """Restaurant area model for organizing tables"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    is_smoking_allowed = models.BooleanField(default=False)
    is_outdoor = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    """Restaurant table model"""
    TABLE_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Being Cleaned'),
        ('maintenance', 'Under Maintenance'),
    ]

    table_number = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(RestaurantArea, on_delete=models.CASCADE, related_name='tables')
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=TABLE_STATUS_CHOICES, default='available')
    location_description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['area', 'table_number']

    def __str__(self):
        return f"Table {self.table_number} - {self.area.name}"

    @property
    def is_available(self):
        return self.status == 'available' and self.is_active

class MenuCategory(models.Model):
    """Menu category model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_categories/', null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Menu Categories'

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """Menu item model"""
    ITEM_TYPE_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('salad', 'Salad'),
        ('soup', 'Soup'),
        ('side_dish', 'Side Dish'),
    ]

    DIETARY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('nut_free', 'Nut Free'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    dietary_info = models.CharField(max_length=20, choices=DIETARY_CHOICES, blank=True)
    ingredients = models.TextField(blank=True, help_text="List main ingredients")
    allergen_info = models.TextField(blank=True, help_text="Allergen information")
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    calories = models.PositiveIntegerField(null=True, blank=True)
    spice_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True,
        help_text="Spice level from 1 (mild) to 5 (very hot)"
    )
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_chef_special = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'display_order', 'name']

    def __str__(self):
        return f"{self.name} - ${self.price}"

    @property
    def profit_margin(self):
        if self.cost_price:
            return ((self.price - self.cost_price) / self.price) * 100
        return None

class TableReservation(models.Model):
    """Table reservation model"""
    RESERVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    reservation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table_reservations')
    guest_count = models.PositiveIntegerField()
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    duration_hours = models.PositiveIntegerField(default=2)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reservation_date', 'reservation_time']

    def __str__(self):
        return f"{self.customer_name} - Table {self.table.table_number} - {self.reservation_date}"

class Order(models.Model):
    """Restaurant order model"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    ORDER_TYPE_CHOICES = [
        ('dine_in', 'Dine In'),
        ('room_service', 'Room Service'),
        ('takeaway', 'Takeaway'),
        ('delivery', 'Delivery'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurant_orders')
    guest_name = models.CharField(max_length=200, blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurant_orders')
    room_number = models.CharField(max_length=20, blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='dine_in')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    guest_count = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_instructions = models.TextField(blank=True)
    estimated_preparation_time = models.PositiveIntegerField(null=True, blank=True)
    actual_preparation_time = models.PositiveIntegerField(null=True, blank=True)
    order_taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taken_orders')
    prepared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prepared_orders')
    served_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='served_orders')
    order_time = models.DateTimeField(default=timezone.now)
    ready_time = models.DateTimeField(null=True, blank=True)
    served_time = models.DateTimeField(null=True, blank=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_time']

    def __str__(self):
        return f"Order {self.order_number} - {self.guest_name or self.customer}"

    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item.total_price for item in self.order_items.all())
        
        # Calculate tax (assuming 10% tax rate)
        self.tax_amount = self.subtotal * 0.10
        
        # Calculate service charge (5% for dine-in)
        if self.order_type == 'dine_in':
            self.service_charge = self.subtotal * 0.05
        
        self.total_amount = self.subtotal + self.tax_amount + self.service_charge - self.discount_amount
        return self.total_amount

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            last_order = Order.objects.filter(
                order_time__date=timezone.now().date()
            ).order_by('-id').first()
            
            if last_order and last_order.order_number:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{new_number:04d}"
        
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Order item model"""
    ITEM_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default='pending')
    preparation_start_time = models.DateTimeField(null=True, blank=True)
    ready_time = models.DateTimeField(null=True, blank=True)
    served_time = models.DateTimeField(null=True, blank=True)
    prepared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class Bill(models.Model):
    """Restaurant bill model"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('room_charge', 'Charge to Room'),
        ('bank_transfer', 'Bank Transfer'),
        ('digital_wallet', 'Digital Wallet'),
    ]

    bill_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bill_number = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tip_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Bill {self.bill_number} - ${self.total_amount}"

    def calculate_balance(self):
        self.balance_due = self.total_amount - self.amount_paid
        if self.balance_due <= 0:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'
        return self.balance_due

    def save(self, *args, **kwargs):
        if not self.bill_number:
            # Generate bill number
            last_bill = Bill.objects.filter(
                generated_at__date=timezone.now().date()
            ).order_by('-id').first()
            
            if last_bill and last_bill.bill_number:
                last_number = int(last_bill.bill_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.bill_number = f"BILL-{timezone.now().strftime('%Y%m%d')}-{new_number:04d}"
        
        self.calculate_balance()
        super().save(*args, **kwargs)

class Inventory(models.Model):
    """Restaurant inventory model"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pieces', 'Pieces'),
        ('packets', 'Packets'),
        ('bottles', 'Bottles'),
        ('cans', 'Cans'),
    ]

    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True)
    supplier_contact = models.CharField(max_length=100, blank=True)
    last_purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    storage_location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['item_name']
        verbose_name_plural = 'Inventory'

    def __str__(self):
        return f"{self.item_name} - {self.current_stock} {self.unit}"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock

    @property
    def stock_value(self):
        return self.current_stock * self.unit_cost

class StockMovement(models.Model):
    """Stock movement tracking"""
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('waste', 'Waste'),
        ('transfer', 'Transfer'),
    ]

    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movement_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-movement_date']

    def __str__(self):
        return f"{self.inventory_item.item_name} - {self.movement_type} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.unit_cost:
            self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

class MenuItemInventory(models.Model):
    """Relationship between menu items and inventory ingredients"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ingredients_used')
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='used_in_menu_items')
    quantity_required = models.DecimalField(max_digits=8, decimal_places=3)
    is_optional = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['menu_item', 'inventory_item']

    def __str__(self):
        return f"{self.menu_item.name} - {self.inventory_item.item_name}"
