from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'templates', views.SMSTemplateViewSet)
router.register(r'campaigns', views.SMSCampaignViewSet)
router.register(r'messages', views.SMSMessageViewSet)
router.register(r'automation-rules', views.SMSAutomationRuleViewSet)
router.register(r'providers', views.SMSProviderViewSet)
router.register(r'blacklist', views.SMSBlacklistViewSet)
router.register(r'delivery-reports', views.SMSDeliveryReportViewSet)
router.register(r'statistics', views.SMSStatisticsViewSet)

app_name = 'sms_service'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # SMS dashboard
    path('dashboard/', views.sms_dashboard, name='dashboard'),
    path('overview/', views.sms_overview, name='overview'),
    
    # Template management
    path('templates/', views.templates_view, name='templates'),
    path('templates/create/', views.create_template, name='create_template'),
    path('templates/<int:template_id>/', views.template_detail, name='template_detail'),
    path('templates/<int:template_id>/edit/', views.edit_template, name='edit_template'),
    path('templates/<int:template_id>/test/', views.test_template, name='test_template'),
    path('templates/<int:template_id>/preview/', views.preview_template, name='preview_template'),
    
    # Campaign management
    path('campaigns/', views.campaigns_view, name='campaigns'),
    path('campaigns/create/', views.create_campaign, name='create_campaign'),
    path('campaigns/<uuid:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<uuid:campaign_id>/edit/', views.edit_campaign, name='edit_campaign'),
    path('campaigns/<uuid:campaign_id>/schedule/', views.schedule_campaign, name='schedule_campaign'),
    path('campaigns/<uuid:campaign_id>/send/', views.send_campaign, name='send_campaign'),
    path('campaigns/<uuid:campaign_id>/cancel/', views.cancel_campaign, name='cancel_campaign'),
    path('campaigns/<uuid:campaign_id>/pause/', views.pause_campaign, name='pause_campaign'),
    path('campaigns/<uuid:campaign_id>/resume/', views.resume_campaign, name='resume_campaign'),
    
    # Message management
    path('messages/', views.messages_view, name='messages'),
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/bulk-send/', views.bulk_send_messages, name='bulk_send_messages'),
    path('messages/<uuid:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<uuid:message_id>/retry/', views.retry_message, name='retry_message'),
    path('messages/<uuid:message_id>/cancel/', views.cancel_message, name='cancel_message'),
    path('messages/queue/', views.message_queue, name='message_queue'),
    path('messages/failed/', views.failed_messages, name='failed_messages'),
    
    # Automation rules
    path('automation/', views.automation_view, name='automation'),
    path('automation/rules/', views.automation_rules, name='automation_rules'),
    path('automation/rules/create/', views.create_automation_rule, name='create_automation_rule'),
    path('automation/rules/<int:rule_id>/', views.automation_rule_detail, name='automation_rule_detail'),
    path('automation/rules/<int:rule_id>/edit/', views.edit_automation_rule, name='edit_automation_rule'),
    path('automation/rules/<int:rule_id>/test/', views.test_automation_rule, name='test_automation_rule'),
    path('automation/rules/<int:rule_id>/toggle/', views.toggle_automation_rule, name='toggle_automation_rule'),
    
    # Provider management
    path('providers/', views.providers_view, name='providers'),
    path('providers/create/', views.create_provider, name='create_provider'),
    path('providers/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('providers/<int:provider_id>/edit/', views.edit_provider, name='edit_provider'),
    path('providers/<int:provider_id>/test/', views.test_provider, name='test_provider'),
    path('providers/<int:provider_id>/set-primary/', views.set_primary_provider, name='set_primary_provider'),
    path('providers/<int:provider_id>/reset-usage/', views.reset_provider_usage, name='reset_provider_usage'),
    
    # Blacklist management
    path('blacklist/', views.blacklist_view, name='blacklist'),
    path('blacklist/add/', views.add_to_blacklist, name='add_to_blacklist'),
    path('blacklist/<int:blacklist_id>/remove/', views.remove_from_blacklist, name='remove_from_blacklist'),
    path('blacklist/import/', views.import_blacklist, name='import_blacklist'),
    path('blacklist/export/', views.export_blacklist, name='export_blacklist'),
    
    # Reports and analytics
    path('reports/', views.sms_reports, name='reports'),
    path('reports/delivery/', views.delivery_report, name='delivery_report'),
    path('reports/campaign-performance/', views.campaign_performance_report, name='campaign_performance_report'),
    path('reports/cost-analysis/', views.cost_analysis_report, name='cost_analysis_report'),
    path('reports/provider-comparison/', views.provider_comparison_report, name='provider_comparison_report'),
    path('reports/automation-effectiveness/', views.automation_effectiveness_report, name='automation_effectiveness_report'),
    
    # Statistics and monitoring
    path('statistics/', views.statistics_view, name='statistics'),
    path('statistics/daily/', views.daily_statistics, name='daily_statistics'),
    path('statistics/monthly/', views.monthly_statistics, name='monthly_statistics'),
    path('statistics/real-time/', views.real_time_statistics, name='real_time_statistics'),
    
    # Settings
    path('settings/', views.sms_settings, name='settings'),
    path('settings/update/', views.update_settings, name='update_settings'),
    path('settings/quiet-hours/', views.quiet_hours_settings, name='quiet_hours_settings'),
    path('settings/rate-limiting/', views.rate_limiting_settings, name='rate_limiting_settings'),
    path('settings/cost-alerts/', views.cost_alert_settings, name='cost_alert_settings'),
    
    # Webhooks
    path('webhooks/twilio/', views.twilio_webhook, name='twilio_webhook'),
    path('webhooks/delivery-status/', views.delivery_status_webhook, name='delivery_status_webhook'),
    path('webhooks/incoming/', views.incoming_sms_webhook, name='incoming_sms_webhook'),
    
    # Quick actions
    path('quick-send/', views.quick_send_sms, name='quick_send_sms'),
    path('reservation-sms/', views.send_reservation_sms, name='send_reservation_sms'),
    path('birthday-sms/', views.send_birthday_sms, name='send_birthday_sms'),
    path('promotional-sms/', views.send_promotional_sms, name='send_promotional_sms'),
    
    # Customer opt-in/opt-out
    path('opt-in/', views.customer_opt_in, name='customer_opt_in'),
    path('opt-out/', views.customer_opt_out, name='customer_opt_out'),
    path('opt-status/<str:phone_number>/', views.opt_status, name='opt_status'),
    
    # Mobile API endpoints
    path('mobile/send/', views.mobile_send_sms, name='mobile_send_sms'),
    path('mobile/templates/', views.mobile_templates, name='mobile_templates'),
    path('mobile/quick-messages/', views.mobile_quick_messages, name='mobile_quick_messages'),
    
    # AJAX endpoints
    path('ajax/template-preview/', views.ajax_template_preview, name='ajax_template_preview'),
    path('ajax/campaign-stats/', views.ajax_campaign_stats, name='ajax_campaign_stats'),
    path('ajax/message-status/', views.ajax_message_status, name='ajax_message_status'),
    path('ajax/provider-status/', views.ajax_provider_status, name='ajax_provider_status'),
    path('ajax/send-test-message/', views.ajax_send_test_message, name='ajax_send_test_message'),
    path('ajax/customer-lookup/', views.ajax_customer_lookup, name='ajax_customer_lookup'),
    
    # Export and import
    path('export/messages/', views.export_messages, name='export_messages'),
    path('export/campaigns/', views.export_campaigns, name='export_campaigns'),
    path('export/statistics/', views.export_statistics, name='export_statistics'),
    path('import/templates/', views.import_templates, name='import_templates'),
    path('import/contacts/', views.import_contacts, name='import_contacts'),
]