from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from hotel_management.models import Customer, Reservation
import uuid

class SMSTemplate(models.Model):
    """SMS message templates for different hotel events"""
    TEMPLATE_TYPE_CHOICES = [
        ('reservation_confirmation', 'Reservation Confirmation'),
        ('checkin_reminder', 'Check-in Reminder'),
        ('checkout_reminder', 'Check-out Reminder'),
        ('welcome_message', 'Welcome Message'),
        ('payment_reminder', 'Payment Reminder'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('room_ready', 'Room Ready Notification'),
        ('restaurant_booking', 'Restaurant Booking'),
        ('service_reminder', 'Service Reminder'),
        ('birthday_wishes', 'Birthday Wishes'),
        ('special_offer', 'Special Offer'),
        ('feedback_request', 'Feedback Request'),
        ('emergency_alert', 'Emergency Alert'),
        ('custom', 'Custom Message'),
    ]

    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPE_CHOICES)
    subject = models.CharField(max_length=100, blank=True)
    message_template = models.TextField(
        help_text="Use variables like {customer_name}, {room_number}, {check_in_date}, etc."
    )
    is_active = models.BooleanField(default=True)
    auto_send = models.BooleanField(default=False, help_text="Automatically send based on triggers")
    send_delay_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Delay before sending (in minutes)"
    )
    language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('ar', 'Arabic'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['template_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

    def get_available_variables(self):
        """Return list of available template variables"""
        variables = [
            '{customer_name}', '{first_name}', '{last_name}',
            '{room_number}', '{room_type}', '{check_in_date}',
            '{check_out_date}', '{reservation_id}', '{total_amount}',
            '{hotel_name}', '{hotel_phone}', '{hotel_address}',
            '{current_date}', '{current_time}', '{confirmation_code}',
        ]
        return variables

class SMSCampaign(models.Model):
    """SMS marketing campaigns"""
    CAMPAIGN_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    RECIPIENT_TYPE_CHOICES = [
        ('all_customers', 'All Customers'),
        ('active_guests', 'Active Guests'),
        ('past_guests', 'Past Guests'),
        ('vip_customers', 'VIP Customers'),
        ('birthday_customers', 'Birthday Customers'),
        ('custom_list', 'Custom List'),
    ]

    campaign_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE, related_name='campaigns')
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES)
    custom_recipients = models.ManyToManyField(Customer, blank=True, related_name='sms_campaigns')
    scheduled_send_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS_CHOICES, default='draft')
    total_recipients = models.PositiveIntegerField(default=0)
    messages_sent = models.PositiveIntegerField(default=0)
    messages_delivered = models.PositiveIntegerField(default=0)
    messages_failed = models.PositiveIntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class SMSMessage(models.Model):
    """Individual SMS messages sent"""
    MESSAGE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    MESSAGE_TYPE_CHOICES = [
        ('transactional', 'Transactional'),
        ('promotional', 'Promotional'),
        ('notification', 'Notification'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ]

    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient_name = models.CharField(max_length=200)
    recipient_phone = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_messages')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='sms_messages')
    campaign = models.ForeignKey(SMSCampaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    template = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='transactional')
    subject = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS_CHOICES, default='pending')
    scheduled_send_time = models.DateTimeField(null=True, blank=True)
    sent_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    external_message_id = models.CharField(max_length=100, blank=True, help_text="Provider's message ID")
    cost = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    sender_id = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"SMS to {self.recipient_name} - {self.get_status_display()}"

    @property
    def can_retry(self):
        return self.status == 'failed' and self.retry_count < self.max_retries

class SMSAutomationRule(models.Model):
    """Rules for automated SMS sending"""
    TRIGGER_EVENT_CHOICES = [
        ('reservation_created', 'Reservation Created'),
        ('reservation_confirmed', 'Reservation Confirmed'),
        ('checkin_due', 'Check-in Due'),
        ('checkout_due', 'Check-out Due'),
        ('payment_due', 'Payment Due'),
        ('payment_received', 'Payment Received'),
        ('birthday', 'Customer Birthday'),
        ('anniversary', 'Stay Anniversary'),
        ('room_ready', 'Room Ready'),
        ('service_request', 'Service Request'),
        ('complaint_received', 'Complaint Received'),
        ('feedback_request', 'Feedback Request'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trigger_event = models.CharField(max_length=30, choices=TRIGGER_EVENT_CHOICES)
    template = models.ForeignKey(SMSTemplate, on_delete=models.CASCADE, related_name='automation_rules')
    delay_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Delay after trigger event (in minutes)"
    )
    conditions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional conditions for triggering (JSON format)"
    )
    is_active = models.BooleanField(default=True)
    applies_to_vip_only = models.BooleanField(default=False)
    max_sends_per_customer = models.PositiveIntegerField(
        default=1,
        help_text="Maximum times to send this message to the same customer"
    )
    time_restrictions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Time restrictions for sending (e.g., only between 9 AM - 6 PM)"
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['trigger_event', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_trigger_event_display()}"

class SMSProvider(models.Model):
    """SMS service provider configuration"""
    PROVIDER_TYPE_CHOICES = [
        ('twilio', 'Twilio'),
        ('aws_sns', 'AWS SNS'),
        ('nexmo', 'Nexmo/Vonage'),
        ('clickatell', 'Clickatell'),
        ('textmagic', 'TextMagic'),
        ('custom', 'Custom Provider'),
    ]

    name = models.CharField(max_length=100)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPE_CHOICES)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    api_endpoint = models.URLField(blank=True)
    account_sid = models.CharField(max_length=100, blank=True)
    auth_token = models.CharField(max_length=100, blank=True)
    sender_id = models.CharField(max_length=20, blank=True)
    webhook_url = models.URLField(blank=True)
    cost_per_message = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    max_message_length = models.PositiveIntegerField(default=160)
    supports_unicode = models.BooleanField(default=True)
    supported_countries = models.TextField(
        blank=True,
        help_text="Comma-separated list of supported country codes"
    )
    daily_limit = models.PositiveIntegerField(null=True, blank=True)
    monthly_limit = models.PositiveIntegerField(null=True, blank=True)
    current_daily_usage = models.PositiveIntegerField(default=0)
    current_monthly_usage = models.PositiveIntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional provider-specific configuration"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    def is_within_limits(self):
        """Check if provider is within usage limits"""
        if self.daily_limit and self.current_daily_usage >= self.daily_limit:
            return False
        if self.monthly_limit and self.current_monthly_usage >= self.monthly_limit:
            return False
        return True

class SMSBlacklist(models.Model):
    """Phone numbers that have opted out of SMS"""
    phone_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=20, choices=[
        ('opted_out', 'Opted Out'),
        ('invalid_number', 'Invalid Number'),
        ('spam_complaint', 'Spam Complaint'),
        ('manual_block', 'Manual Block'),
    ], default='opted_out')
    blocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    blocked_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-blocked_date']

    def __str__(self):
        return f"Blocked: {self.phone_number}"

class SMSDeliveryReport(models.Model):
    """Delivery reports and webhooks from SMS providers"""
    message = models.ForeignKey(SMSMessage, on_delete=models.CASCADE, related_name='delivery_reports')
    external_message_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    delivery_time = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=20, blank=True)
    error_message = models.TextField(blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    webhook_received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-webhook_received_at']

    def __str__(self):
        return f"Report for {self.message.message_id} - {self.status}"

class SMSStatistics(models.Model):
    """Daily SMS statistics"""
    date = models.DateField(unique=True)
    total_sent = models.PositiveIntegerField(default=0)
    total_delivered = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transactional_count = models.PositiveIntegerField(default=0)
    promotional_count = models.PositiveIntegerField(default=0)
    notification_count = models.PositiveIntegerField(default=0)
    reminder_count = models.PositiveIntegerField(default=0)
    alert_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"SMS Stats - {self.date} - {self.total_sent} sent"

    @property
    def delivery_rate(self):
        if self.total_sent > 0:
            return (self.total_delivered / self.total_sent) * 100
        return 0

    @property
    def failure_rate(self):
        if self.total_sent > 0:
            return (self.total_failed / self.total_sent) * 100
        return 0

class SMSSettings(models.Model):
    """Global SMS system settings"""
    default_sender_id = models.CharField(max_length=20, default='HOTEL')
    enable_auto_messaging = models.BooleanField(default=True)
    enable_delivery_reports = models.BooleanField(default=True)
    default_retry_attempts = models.PositiveIntegerField(default=3)
    retry_delay_minutes = models.PositiveIntegerField(default=30)
    max_message_length = models.PositiveIntegerField(default=160)
    enable_unicode = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(default='22:00')
    quiet_hours_end = models.TimeField(default='08:00')
    enable_quiet_hours = models.BooleanField(default=True)
    opt_out_keywords = models.TextField(
        default='STOP,UNSUBSCRIBE,OPTOUT',
        help_text="Comma-separated list of opt-out keywords"
    )
    opt_in_keywords = models.TextField(
        default='START,SUBSCRIBE,OPTIN',
        help_text="Comma-separated list of opt-in keywords"
    )
    enable_double_opt_in = models.BooleanField(default=False)
    webhook_secret = models.CharField(max_length=100, blank=True)
    enable_rate_limiting = models.BooleanField(default=True)
    rate_limit_per_minute = models.PositiveIntegerField(default=100)
    enable_cost_alerts = models.BooleanField(default=True)
    daily_cost_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    monthly_cost_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SMS Settings"
        verbose_name_plural = "SMS Settings"

    def __str__(self):
        return "SMS System Settings"

    def is_quiet_hours(self, check_time=None):
        """Check if current time is within quiet hours"""
        if not self.enable_quiet_hours:
            return False
        
        if not check_time:
            check_time = timezone.now().time()
        
        if self.quiet_hours_start <= self.quiet_hours_end:
            # Same day quiet hours (e.g., 22:00 to 08:00 next day)
            return self.quiet_hours_start <= check_time <= self.quiet_hours_end
        else:
            # Overnight quiet hours (e.g., 22:00 to 08:00)
            return check_time >= self.quiet_hours_start or check_time <= self.quiet_hours_end

class SMSWebhookLog(models.Model):
    """Log of webhook events received from SMS providers"""
    provider = models.ForeignKey(SMSProvider, on_delete=models.CASCADE, related_name='webhook_logs')
    external_message_id = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"Webhook - {self.provider.name} - {self.event_type}"
