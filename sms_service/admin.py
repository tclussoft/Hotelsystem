from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    SMSTemplate, SMSCampaign, SMSMessage, SMSAutomationRule, SMSProvider,
    SMSBlacklist, SMSDeliveryReport, SMSStatistics, SMSSettings, SMSWebhookLog
)

@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'language', 'is_active', 'auto_send', 'created_by', 'created_at']
    list_filter = ['template_type', 'language', 'is_active', 'auto_send', 'created_at']
    search_fields = ['name', 'subject', 'message_template']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_type', 'subject', 'language')
        }),
        ('Message Content', {
            'fields': ('message_template',)
        }),
        ('Settings', {
            'fields': ('is_active', 'auto_send', 'send_delay_minutes')
        }),
        ('Created By', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Show available variables as help text
            variables = obj.get_available_variables()
            form.base_fields['message_template'].help_text = f"Available variables: {', '.join(variables)}"
        return form

@admin.register(SMSCampaign)
class SMSCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'template', 'recipient_type', 'status', 'total_recipients', 'messages_sent', 'delivery_rate', 'scheduled_send_time']
    list_filter = ['status', 'recipient_type', 'scheduled_send_time', 'created_at']
    search_fields = ['name', 'description', 'campaign_id']
    readonly_fields = ['campaign_id', 'total_recipients', 'messages_sent', 'messages_delivered', 'messages_failed', 'delivery_rate', 'created_at', 'updated_at']
    filter_horizontal = ['custom_recipients']
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('campaign_id', 'name', 'description', 'template')
        }),
        ('Recipients', {
            'fields': ('recipient_type', 'custom_recipients')
        }),
        ('Schedule', {
            'fields': ('scheduled_send_time', 'status')
        }),
        ('Statistics', {
            'fields': ('total_recipients', 'messages_sent', 'messages_delivered', 'messages_failed', 'delivery_rate')
        }),
        ('Cost', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Created By', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )
    
    def delivery_rate(self, obj):
        if obj.messages_sent > 0:
            rate = (obj.messages_delivered / obj.messages_sent) * 100
            return f"{rate:.1f}%"
        return "0%"
    delivery_rate.short_description = 'Delivery Rate'

@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id_short', 'recipient_name', 'recipient_phone', 'message_type', 'status', 'sent_time', 'cost']
    list_filter = ['message_type', 'status', 'sent_time', 'campaign', 'template']
    search_fields = ['message_id', 'recipient_name', 'recipient_phone', 'content', 'external_message_id']
    readonly_fields = ['message_id', 'external_message_id', 'sent_time', 'delivered_time', 'created_at', 'updated_at']
    date_hierarchy = 'sent_time'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('message_id', 'message_type', 'template', 'campaign')
        }),
        ('Recipient', {
            'fields': ('recipient_name', 'recipient_phone', 'customer', 'reservation')
        }),
        ('Content', {
            'fields': ('subject', 'content')
        }),
        ('Delivery', {
            'fields': ('status', 'scheduled_send_time', 'sent_time', 'delivered_time', 'external_message_id')
        }),
        ('Cost & Retry', {
            'fields': ('cost', 'retry_count', 'max_retries')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Created By', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )
    
    def message_id_short(self, obj):
        return str(obj.message_id)[:8] + '...'
    message_id_short.short_description = 'Message ID'

@admin.register(SMSAutomationRule)
class SMSAutomationRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_event', 'template', 'delay_minutes', 'is_active', 'applies_to_vip_only', 'max_sends_per_customer']
    list_filter = ['trigger_event', 'is_active', 'applies_to_vip_only', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Rule Information', {
            'fields': ('name', 'description', 'trigger_event', 'template')
        }),
        ('Timing', {
            'fields': ('delay_minutes', 'time_restrictions')
        }),
        ('Conditions', {
            'fields': ('conditions', 'applies_to_vip_only', 'max_sends_per_customer')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Created By', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )

@admin.register(SMSProvider)
class SMSProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_type', 'is_primary', 'is_active', 'current_daily_usage', 'daily_limit', 'is_within_limits']
    list_filter = ['provider_type', 'is_primary', 'is_active', 'supports_unicode']
    search_fields = ['name', 'account_sid', 'sender_id']
    readonly_fields = ['current_daily_usage', 'current_monthly_usage', 'last_reset_date', 'is_within_limits', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Provider Information', {
            'fields': ('name', 'provider_type', 'is_primary', 'is_active')
        }),
        ('API Configuration', {
            'fields': ('api_endpoint', 'account_sid', 'auth_token', 'sender_id', 'webhook_url')
        }),
        ('Capabilities', {
            'fields': ('cost_per_message', 'max_message_length', 'supports_unicode', 'supported_countries')
        }),
        ('Usage Limits', {
            'fields': ('daily_limit', 'monthly_limit', 'current_daily_usage', 'current_monthly_usage', 'last_reset_date')
        }),
        ('Configuration', {
            'fields': ('configuration',),
            'classes': ('collapse',)
        })
    )
    
    def is_within_limits(self, obj):
        return obj.is_within_limits()
    is_within_limits.boolean = True
    is_within_limits.short_description = 'Within Limits'

@admin.register(SMSBlacklist)
class SMSBlacklistAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'customer', 'reason', 'blocked_by', 'blocked_date']
    list_filter = ['reason', 'blocked_date']
    search_fields = ['phone_number', 'customer__first_name', 'customer__last_name', 'notes']
    readonly_fields = ['blocked_date']

@admin.register(SMSDeliveryReport)
class SMSDeliveryReportAdmin(admin.ModelAdmin):
    list_display = ['message_link', 'external_message_id', 'status', 'delivery_time', 'error_code', 'webhook_received_at']
    list_filter = ['status', 'delivery_time', 'webhook_received_at']
    search_fields = ['external_message_id', 'error_code', 'error_message']
    readonly_fields = ['webhook_received_at']
    
    def message_link(self, obj):
        if obj.message:
            url = reverse('admin:sms_service_smsmessage_change', args=[obj.message.pk])
            return format_html('<a href="{}">{}</a>', url, str(obj.message.message_id)[:8] + '...')
        return 'N/A'
    message_link.short_description = 'Message'

@admin.register(SMSStatistics)
class SMSStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sent', 'total_delivered', 'total_failed', 'delivery_rate', 'failure_rate', 'total_cost']
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['delivery_rate', 'failure_rate', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    
    def delivery_rate(self, obj):
        return f"{obj.delivery_rate:.1f}%"
    delivery_rate.short_description = 'Delivery Rate'
    
    def failure_rate(self, obj):
        return f"{obj.failure_rate:.1f}%"
    failure_rate.short_description = 'Failure Rate'

@admin.register(SMSSettings)
class SMSSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_sender_id', 'enable_auto_messaging', 'enable_delivery_reports', 'default_retry_attempts', 'enable_quiet_hours']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Basic Settings', {
            'fields': ('default_sender_id', 'enable_auto_messaging', 'enable_delivery_reports')
        }),
        ('Retry Settings', {
            'fields': ('default_retry_attempts', 'retry_delay_minutes')
        }),
        ('Message Settings', {
            'fields': ('max_message_length', 'enable_unicode')
        }),
        ('Quiet Hours', {
            'fields': ('enable_quiet_hours', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Opt-out Management', {
            'fields': ('opt_out_keywords', 'opt_in_keywords', 'enable_double_opt_in')
        }),
        ('Rate Limiting', {
            'fields': ('enable_rate_limiting', 'rate_limit_per_minute')
        }),
        ('Cost Monitoring', {
            'fields': ('enable_cost_alerts', 'daily_cost_threshold', 'monthly_cost_threshold')
        }),
        ('Security', {
            'fields': ('webhook_secret',)
        }),
        ('Last Updated', {
            'fields': ('updated_by', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one instance of settings
        return not SMSSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False

@admin.register(SMSWebhookLog)
class SMSWebhookLogAdmin(admin.ModelAdmin):
    list_display = ['provider', 'event_type', 'external_message_id', 'processed', 'received_at', 'processed_at']
    list_filter = ['provider', 'event_type', 'processed', 'received_at']
    search_fields = ['external_message_id', 'event_type', 'processing_error']
    readonly_fields = ['received_at', 'processed_at']
    
    def get_readonly_fields(self, request, obj=None):
        # Make payload field readonly with formatted JSON
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly.append('payload_formatted')
        return readonly
    
    def payload_formatted(self, obj):
        import json
        try:
            formatted = json.dumps(obj.payload, indent=2)
            return mark_safe(f'<pre>{formatted}</pre>')
        except:
            return str(obj.payload)
    payload_formatted.short_description = 'Payload (Formatted)'
