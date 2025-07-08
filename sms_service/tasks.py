from celery import shared_task
from django.utils import timezone
from django.template import Template, Context
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import logging
from datetime import datetime, timedelta
from .models import (
    SMSMessage, SMSTemplate, SMSCampaign, SMSAutomationRule, SMSProvider,
    SMSBlacklist, SMSSettings, SMSStatistics, SMSDeliveryReport
)
from hotel_management.models import Reservation, Customer
from employees.models import Employee

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms_message(self, message_id):
    """Send individual SMS message using Twilio"""
    try:
        message = SMSMessage.objects.get(id=message_id)
        
        # Check if message is already sent
        if message.status in ['sent', 'delivered']:
            logger.info(f"Message {message.message_id} already sent")
            return
        
        # Check blacklist
        if SMSBlacklist.objects.filter(phone_number=message.recipient_phone).exists():
            message.status = 'cancelled'
            message.error_message = 'Phone number is blacklisted'
            message.save()
            logger.warning(f"Message {message.message_id} cancelled - blacklisted number")
            return
        
        # Get SMS settings
        sms_settings = SMSSettings.objects.first()
        if not sms_settings or not sms_settings.enable_auto_messaging:
            logger.warning("SMS auto messaging is disabled")
            return
        
        # Check quiet hours
        if sms_settings.is_quiet_hours():
            # Reschedule for after quiet hours
            schedule_time = timezone.now() + timedelta(hours=1)
            send_sms_message.apply_async(args=[message_id], eta=schedule_time)
            logger.info(f"Message {message.message_id} rescheduled due to quiet hours")
            return
        
        # Get primary SMS provider
        provider = SMSProvider.objects.filter(is_primary=True, is_active=True).first()
        if not provider:
            logger.error("No active SMS provider found")
            return
        
        # Check provider limits
        if not provider.is_within_limits():
            logger.error(f"Provider {provider.name} has exceeded limits")
            return
        
        # Initialize Twilio client
        if provider.provider_type == 'twilio':
            client = Client(provider.account_sid, provider.auth_token)
            
            try:
                # Send SMS
                twilio_message = client.messages.create(
                    body=message.content,
                    from_=provider.sender_id or settings.TWILIO_PHONE_NUMBER,
                    to=message.recipient_phone
                )
                
                # Update message status
                message.status = 'sent'
                message.sent_time = timezone.now()
                message.external_message_id = twilio_message.sid
                message.cost = provider.cost_per_message
                message.save()
                
                # Update provider usage
                provider.current_daily_usage += 1
                provider.current_monthly_usage += 1
                provider.save()
                
                logger.info(f"SMS sent successfully: {message.message_id}")
                
            except TwilioException as e:
                message.status = 'failed'
                message.error_message = str(e)
                message.save()
                logger.error(f"Twilio error for message {message.message_id}: {e}")
                
                # Retry if possible
                if message.can_retry:
                    message.retry_count += 1
                    message.save()
                    raise self.retry(countdown=60 * message.retry_count)
        
    except SMSMessage.DoesNotExist:
        logger.error(f"SMS message with ID {message_id} not found")
    except Exception as e:
        logger.error(f"Error sending SMS message {message_id}: {e}")
        raise self.retry(countdown=60)

@shared_task
def send_scheduled_sms():
    """Process and send scheduled SMS messages"""
    now = timezone.now()
    
    # Get messages scheduled to be sent now or in the past
    scheduled_messages = SMSMessage.objects.filter(
        status='queued',
        scheduled_send_time__lte=now
    )
    
    for message in scheduled_messages:
        send_sms_message.delay(message.id)
    
    logger.info(f"Processed {scheduled_messages.count()} scheduled SMS messages")

@shared_task
def process_automation_rules():
    """Process SMS automation rules and trigger messages"""
    now = timezone.now()
    
    # Get active automation rules
    rules = SMSAutomationRule.objects.filter(is_active=True)
    
    for rule in rules:
        try:
            if rule.trigger_event == 'reservation_created':
                # Check for new reservations
                cutoff_time = now - timedelta(minutes=rule.delay_minutes + 5)
                reservations = Reservation.objects.filter(
                    created_at__gte=cutoff_time,
                    status='confirmed'
                )
                
                for reservation in reservations:
                    if not should_send_automated_message(rule, reservation.customer):
                        continue
                    
                    create_automated_sms.delay(rule.id, reservation.id)
            
            elif rule.trigger_event == 'checkin_due':
                # Check for check-ins due today
                today = now.date()
                reservations = Reservation.objects.filter(
                    check_in_date=today,
                    status='confirmed'
                )
                
                for reservation in reservations:
                    if not should_send_automated_message(rule, reservation.customer):
                        continue
                    
                    create_automated_sms.delay(rule.id, reservation.id)
            
            elif rule.trigger_event == 'checkout_due':
                # Check for check-outs due today
                today = now.date()
                reservations = Reservation.objects.filter(
                    check_out_date=today,
                    status='checked_in'
                )
                
                for reservation in reservations:
                    if not should_send_automated_message(rule, reservation.customer):
                        continue
                    
                    create_automated_sms.delay(rule.id, reservation.id)
            
            elif rule.trigger_event == 'birthday':
                # Check for customer birthdays
                today = now.date()
                customers = Customer.objects.filter(
                    date_of_birth__month=today.month,
                    date_of_birth__day=today.day
                )
                
                for customer in customers:
                    if not should_send_automated_message(rule, customer):
                        continue
                    
                    create_birthday_sms.delay(rule.id, customer.id)
        
        except Exception as e:
            logger.error(f"Error processing automation rule {rule.id}: {e}")

def should_send_automated_message(rule, customer):
    """Check if automated message should be sent to customer"""
    # Check VIP restriction
    if rule.applies_to_vip_only:
        # Implement VIP check logic based on your criteria
        # For now, assuming all customers are eligible
        pass
    
    # Check message frequency limits
    recent_messages = SMSMessage.objects.filter(
        customer=customer,
        template=rule.template,
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    if recent_messages >= rule.max_sends_per_customer:
        return False
    
    return True

@shared_task
def create_automated_sms(rule_id, reservation_id):
    """Create automated SMS message from rule and reservation"""
    try:
        rule = SMSAutomationRule.objects.get(id=rule_id)
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Prepare template context
        context = {
            'customer_name': reservation.customer.full_name,
            'first_name': reservation.customer.first_name,
            'last_name': reservation.customer.last_name,
            'room_number': reservation.room.room_number,
            'room_type': reservation.room.room_type.name,
            'check_in_date': reservation.check_in_date.strftime('%Y-%m-%d'),
            'check_out_date': reservation.check_out_date.strftime('%Y-%m-%d'),
            'reservation_id': str(reservation.reservation_id)[:8],
            'total_amount': str(reservation.total_amount),
            'hotel_name': settings.HOTEL_NAME,
            'hotel_phone': settings.HOTEL_PHONE,
            'hotel_address': settings.HOTEL_ADDRESS,
            'current_date': timezone.now().strftime('%Y-%m-%d'),
            'current_time': timezone.now().strftime('%H:%M'),
        }
        
        # Render message content
        template = Template(rule.template.message_template)
        content = template.render(Context(context))
        
        # Calculate send time
        send_time = timezone.now() + timedelta(minutes=rule.delay_minutes)
        
        # Create SMS message
        message = SMSMessage.objects.create(
            recipient_name=reservation.customer.full_name,
            recipient_phone=reservation.customer.phone_number,
            customer=reservation.customer,
            reservation=reservation,
            template=rule.template,
            message_type='notification',
            content=content,
            status='queued',
            scheduled_send_time=send_time
        )
        
        logger.info(f"Created automated SMS message {message.message_id} for rule {rule.name}")
        
    except Exception as e:
        logger.error(f"Error creating automated SMS for rule {rule_id}: {e}")

@shared_task
def create_birthday_sms(rule_id, customer_id):
    """Create birthday SMS message"""
    try:
        rule = SMSAutomationRule.objects.get(id=rule_id)
        customer = Customer.objects.get(id=customer_id)
        
        # Prepare template context
        context = {
            'customer_name': customer.full_name,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'hotel_name': settings.HOTEL_NAME,
            'hotel_phone': settings.HOTEL_PHONE,
            'current_date': timezone.now().strftime('%Y-%m-%d'),
        }
        
        # Render message content
        template = Template(rule.template.message_template)
        content = template.render(Context(context))
        
        # Create SMS message
        message = SMSMessage.objects.create(
            recipient_name=customer.full_name,
            recipient_phone=customer.phone_number,
            customer=customer,
            template=rule.template,
            message_type='promotional',
            content=content,
            status='queued',
            scheduled_send_time=timezone.now() + timedelta(minutes=rule.delay_minutes)
        )
        
        logger.info(f"Created birthday SMS message {message.message_id} for customer {customer.full_name}")
        
    except Exception as e:
        logger.error(f"Error creating birthday SMS for customer {customer_id}: {e}")

@shared_task
def send_campaign_messages(campaign_id):
    """Send SMS messages for a campaign"""
    try:
        campaign = SMSCampaign.objects.get(id=campaign_id)
        
        if campaign.status != 'scheduled':
            logger.warning(f"Campaign {campaign.name} is not in scheduled status")
            return
        
        # Update campaign status
        campaign.status = 'sending'
        campaign.save()
        
        # Get recipients based on campaign type
        recipients = []
        
        if campaign.recipient_type == 'all_customers':
            recipients = Customer.objects.all()
        elif campaign.recipient_type == 'active_guests':
            today = timezone.now().date()
            active_reservations = Reservation.objects.filter(
                check_in_date__lte=today,
                check_out_date__gte=today,
                status='checked_in'
            )
            recipients = [r.customer for r in active_reservations]
        elif campaign.recipient_type == 'past_guests':
            past_reservations = Reservation.objects.filter(
                status='checked_out'
            ).distinct('customer')
            recipients = [r.customer for r in past_reservations]
        elif campaign.recipient_type == 'birthday_customers':
            today = timezone.now().date()
            recipients = Customer.objects.filter(
                date_of_birth__month=today.month,
                date_of_birth__day=today.day
            )
        elif campaign.recipient_type == 'custom_list':
            recipients = campaign.custom_recipients.all()
        
        # Create messages for each recipient
        for customer in recipients:
            # Check blacklist
            if SMSBlacklist.objects.filter(phone_number=customer.phone_number).exists():
                continue
            
            # Prepare template context
            context = {
                'customer_name': customer.full_name,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'hotel_name': settings.HOTEL_NAME,
                'hotel_phone': settings.HOTEL_PHONE,
                'current_date': timezone.now().strftime('%Y-%m-%d'),
            }
            
            # Render message content
            template = Template(campaign.template.message_template)
            content = template.render(Context(context))
            
            # Create SMS message
            message = SMSMessage.objects.create(
                recipient_name=customer.full_name,
                recipient_phone=customer.phone_number,
                customer=customer,
                campaign=campaign,
                template=campaign.template,
                message_type='promotional',
                content=content,
                status='queued',
                scheduled_send_time=campaign.scheduled_send_time or timezone.now()
            )
        
        # Update campaign totals
        campaign.total_recipients = len(recipients)
        campaign.save()
        
        logger.info(f"Created {len(recipients)} messages for campaign {campaign.name}")
        
    except Exception as e:
        logger.error(f"Error sending campaign messages for campaign {campaign_id}: {e}")

@shared_task
def update_daily_statistics():
    """Update daily SMS statistics"""
    today = timezone.now().date()
    
    try:
        # Get or create today's statistics
        stats, created = SMSStatistics.objects.get_or_create(date=today)
        
        # Count messages by status
        today_messages = SMSMessage.objects.filter(sent_time__date=today)
        
        stats.total_sent = today_messages.filter(status='sent').count()
        stats.total_delivered = today_messages.filter(status='delivered').count()
        stats.total_failed = today_messages.filter(status='failed').count()
        
        # Count by message type
        stats.transactional_count = today_messages.filter(message_type='transactional').count()
        stats.promotional_count = today_messages.filter(message_type='promotional').count()
        stats.notification_count = today_messages.filter(message_type='notification').count()
        stats.reminder_count = today_messages.filter(message_type='reminder').count()
        stats.alert_count = today_messages.filter(message_type='alert').count()
        
        # Calculate total cost
        stats.total_cost = sum(msg.cost for msg in today_messages if msg.cost)
        
        stats.save()
        
        logger.info(f"Updated SMS statistics for {today}")
        
    except Exception as e:
        logger.error(f"Error updating SMS statistics: {e}")

@shared_task
def process_delivery_webhooks():
    """Process pending delivery webhook reports"""
    from .models import SMSWebhookLog
    
    pending_webhooks = SMSWebhookLog.objects.filter(processed=False)
    
    for webhook in pending_webhooks:
        try:
            if webhook.external_message_id:
                message = SMSMessage.objects.filter(
                    external_message_id=webhook.external_message_id
                ).first()
                
                if message:
                    # Update message status based on webhook
                    if webhook.event_type in ['delivered', 'delivery']:
                        message.status = 'delivered'
                        message.delivered_time = timezone.now()
                    elif webhook.event_type in ['failed', 'undelivered']:
                        message.status = 'failed'
                        if 'error' in webhook.payload:
                            message.error_message = webhook.payload.get('error', '')
                    
                    message.save()
                    
                    # Create delivery report
                    SMSDeliveryReport.objects.create(
                        message=message,
                        external_message_id=webhook.external_message_id,
                        status=webhook.event_type,
                        delivery_time=message.delivered_time,
                        provider_response=webhook.payload
                    )
            
            webhook.processed = True
            webhook.processed_at = timezone.now()
            webhook.save()
            
        except Exception as e:
            webhook.processing_error = str(e)
            webhook.save()
            logger.error(f"Error processing webhook {webhook.id}: {e}")

@shared_task
def send_manual_sms(recipient_phone, message_content, message_type='manual'):
    """Send manual SMS message"""
    try:
        # Create SMS message record
        message = SMSMessage.objects.create(
            recipient_name='Manual Recipient',
            recipient_phone=recipient_phone,
            message_type=message_type,
            content=message_content,
            status='queued'
        )
        
        # Send immediately
        send_sms_message.delay(message.id)
        
        return message.message_id
        
    except Exception as e:
        logger.error(f"Error sending manual SMS: {e}")
        raise

@shared_task
def cleanup_old_sms_data():
    """Clean up old SMS data to maintain database performance"""
    try:
        # Delete old messages (older than 1 year)
        cutoff_date = timezone.now() - timedelta(days=365)
        
        old_messages = SMSMessage.objects.filter(created_at__lt=cutoff_date)
        deleted_count = old_messages.count()
        old_messages.delete()
        
        # Delete old delivery reports
        old_reports = SMSDeliveryReport.objects.filter(webhook_received_at__lt=cutoff_date)
        old_reports.delete()
        
        # Delete old webhook logs
        old_webhooks = SMSWebhookLog.objects.filter(received_at__lt=cutoff_date)
        old_webhooks.delete()
        
        logger.info(f"Cleaned up {deleted_count} old SMS messages and related data")
        
    except Exception as e:
        logger.error(f"Error cleaning up SMS data: {e}")

# SMS convenience functions for easy integration
def send_reservation_confirmation(reservation):
    """Send reservation confirmation SMS"""
    template = SMSTemplate.objects.filter(
        template_type='reservation_confirmation',
        is_active=True
    ).first()
    
    if template:
        create_automated_sms.delay(
            SMSAutomationRule.objects.filter(
                trigger_event='reservation_confirmed',
                template=template,
                is_active=True
            ).first().id,
            reservation.id
        )

def send_checkout_reminder(reservation):
    """Send checkout reminder SMS"""
    template = SMSTemplate.objects.filter(
        template_type='checkout_reminder',
        is_active=True
    ).first()
    
    if template:
        create_automated_sms.delay(
            SMSAutomationRule.objects.filter(
                trigger_event='checkout_due',
                template=template,
                is_active=True
            ).first().id,
            reservation.id
        )