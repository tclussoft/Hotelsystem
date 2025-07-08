from django.apps import AppConfig


class SmsServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_service'
    verbose_name = 'SMS Service'