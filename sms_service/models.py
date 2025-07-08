from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from hotel.models import Customer, Reservation
from decimal import Decimal
import uuid

class SMSProvider(models.Model):
    """SMS service providers configuration"""
    name = models.CharField(max_length=100, unique=True)
    provider_type = models.CharField(max_length=50, choices=[
        ('twilio', 'Twilio'),
        ('aws_sns', 'AWS SNS'),
        ('nexmo', 'Nexmo'),
        ('messagebird', 'MessageBird'),
        ('custom', 'Custom Provider')
    ])
    api_key = models.CharField(max_length=200)
    api_secret = models.CharField(max_length=200)
    sender_id = models.CharField(max_length=20)
    base_url = models.URLField(blank=True)
    cost_per_sms = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    monthly_limit = models.PositiveIntegerField(default=0, help_text="0 means unlimited")
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

class SMSTemplate(models.Model):
    """SMS message templates"""
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Message'),
        ('booking_confirmation', 'Booking Confirmation'),
        ('check_in_reminder', 'Check-in Reminder'),
        ('check_out_reminder', 'Check-out Reminder'),
        ('payment_reminder', 'Payment Reminder'),
        ('birthday_wishes', 'Birthday Wishes'),
        ('promotional', 'Promotional'),
        ('feedback_request', 'Feedback Request'),
        ('service_confirmation', 'Service Confirmation'),
        ('emergency_alert', 'Emergency Alert'),
        ('custom', 'Custom Template')
    ]
    
    name = models.CharField(max_length=200, unique=True)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField(help_text="Use variables like {customer_name}, {room_number}, {check_in_date}, etc.")
    variables = models.TextField(blank=True, help_text="Comma-separated list of available variables")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

class SMSCampaign(models.Model):
    """SMS marketing campaigns"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled')
    ]
    
    TARGET_AUDIENCE_CHOICES = [
        ('all_customers', 'All Customers'),
        ('current_guests', 'Current Guests'),
        ('past_guests', 'Past Guests'),
        ('vip_customers', 'VIP Customers'),
        ('birthday_customers', 'Birthday Customers'),
        ('custom_list', 'Custom List')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE)
    target_audience = models.CharField(max_length=30, choices=TARGET_AUDIENCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    total_recipients = models.PositiveIntegerField(default=0)
    messages_sent = models.PositiveIntegerField(default=0)
    messages_delivered = models.PositiveIntegerField(default=0)
    messages_failed = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class AutomationRule(models.Model):
    """SMS automation rules"""
    TRIGGER_EVENTS = [
        ('reservation_created', 'Reservation Created'),
        ('reservation_confirmed', 'Reservation Confirmed'),
        ('check_in', 'Guest Check-in'),
        ('check_out', 'Guest Check-out'),
        ('payment_due', 'Payment Due'),
        ('payment_received', 'Payment Received'),
        ('birthday', 'Customer Birthday'),
        ('anniversary', 'Stay Anniversary'),
        ('feedback_due', 'Feedback Due'),
        ('special_offer', 'Special Offer'),
        ('maintenance_alert', 'Maintenance Alert')
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    trigger_event = models.CharField(max_length=30, choices=TRIGGER_EVENTS)
    template = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE)
    delay_minutes = models.PositiveIntegerField(default=0, help_text="Delay before sending SMS")
    conditions = models.TextField(blank=True, help_text="JSON conditions for triggering")
    is_active = models.BooleanField(default=True)
    send_count = models.PositiveIntegerField(default=0)
    last_triggered = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_trigger_event_display()}"

class SMSMessage(models.Model):
    """Individual SMS messages"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ]
    
    MESSAGE_TYPES = [
        ('manual', 'Manual'),
        ('campaign', 'Campaign'),
        ('automated', 'Automated'),
        ('api', 'API')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient_phone = models.CharField(max_length=20)
    recipient_name = models.CharField(max_length=200, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_messages')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_messages')
    campaign = models.ForeignKey(SMSCampaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    automation_rule = models.ForeignKey(AutomationRule, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    template = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='manual')
    subject = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider = models.ForeignKey(SMSProvider, on_delete=models.SET_NULL, null=True, blank=True)
    provider_message_id = models.CharField(max_length=100, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    sent_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.recipient_phone} - {self.get_status_display()}"

class SMSBlacklist(models.Model):
    """Blacklisted phone numbers that should not receive SMS"""
    phone_number = models.CharField(max_length=20, unique=True)
    reason = models.CharField(max_length=200, choices=[
        ('opt_out', 'Customer Opted Out'),
        ('complaint', 'Customer Complaint'),
        ('invalid', 'Invalid Number'),
        ('spam_report', 'Spam Report'),
        ('admin_block', 'Admin Block')
    ])
    notes = models.TextField(blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Blacklisted: {self.phone_number} - {self.get_reason_display()}"

class SMSDeliveryReport(models.Model):
    """SMS delivery reports from providers"""
    message = models.OneToOneField(SMSMessage, on_delete=models.CASCADE, related_name='delivery_report')
    provider_status = models.CharField(max_length=50)
    provider_error_code = models.CharField(max_length=20, blank=True)
    provider_error_message = models.TextField(blank=True)
    delivery_timestamp = models.DateTimeField()
    segments_count = models.PositiveIntegerField(default=1)
    network_code = models.CharField(max_length=10, blank=True)
    country_code = models.CharField(max_length=5, blank=True)
    raw_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Delivery report for {self.message.recipient_phone}"

class SMSUsageStats(models.Model):
    """Daily SMS usage statistics"""
    date = models.DateField(unique=True)
    total_sent = models.PositiveIntegerField(default=0)
    total_delivered = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    manual_messages = models.PositiveIntegerField(default=0)
    campaign_messages = models.PositiveIntegerField(default=0)
    automated_messages = models.PositiveIntegerField(default=0)
    api_messages = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"SMS Stats for {self.date} - {self.total_sent} sent"

class SMSScheduledMessage(models.Model):
    """Scheduled SMS messages for future sending"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipients = models.TextField(help_text="JSON array of recipient phone numbers")
    template = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE)
    template_variables = models.TextField(blank=True, help_text="JSON object with template variables")
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    total_recipients = models.PositiveIntegerField(default=0)
    messages_created = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_time']
    
    def __str__(self):
        return f"Scheduled SMS - {self.scheduled_time} - {self.total_recipients} recipients"

class SMSOptOut(models.Model):
    """Customers who have opted out of SMS communications"""
    phone_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    opt_out_method = models.CharField(max_length=20, choices=[
        ('reply_stop', 'Reply STOP'),
        ('web_form', 'Web Form'),
        ('phone_call', 'Phone Call'),
        ('admin_action', 'Admin Action')
    ])
    opt_out_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-opt_out_date']
    
    def __str__(self):
        return f"Opted out: {self.phone_number}"

class SMSCostAnalysis(models.Model):
    """Monthly SMS cost analysis"""
    month = models.DateField()
    provider = models.ForeignKey(SMSProvider, on_delete=models.CASCADE)
    total_messages = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    average_cost_per_message = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['month', 'provider']
        ordering = ['-month']
    
    def __str__(self):
        return f"Cost analysis for {self.provider.name} - {self.month.strftime('%B %Y')}"