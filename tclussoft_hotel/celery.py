import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tclussoft_hotel.settings')

app = Celery('tclussoft_hotel')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'send-scheduled-sms': {
        'task': 'sms_service.tasks.send_scheduled_sms',
        'schedule': 60.0,  # Run every minute
    },
    'process-automation-rules': {
        'task': 'sms_service.tasks.process_automation_rules',
        'schedule': 300.0,  # Run every 5 minutes
    },
    'check-overdue-checkouts': {
        'task': 'hotel_management.tasks.check_overdue_checkouts',
        'schedule': 3600.0,  # Run every hour
    },
    'generate-daily-reports': {
        'task': 'hotel_management.tasks.generate_daily_reports',
        'schedule': 86400.0,  # Run once a day
    },
    'process-payroll': {
        'task': 'employees.tasks.process_monthly_payroll',
        'schedule': 86400.0,  # Run once a day
    },
    'update-sms-statistics': {
        'task': 'sms_service.tasks.update_daily_statistics',
        'schedule': 3600.0,  # Run every hour
    },
    'cleanup-old-data': {
        'task': 'hotel_management.tasks.cleanup_old_data',
        'schedule': 86400.0,  # Run once a day
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')