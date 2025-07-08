#!/usr/bin/env python
"""
Tclussoft Hotel Management System Setup Script
This script will help set up the hotel management system properly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tclussoft_hotel.settings')

def setup_django():
    """Initialize Django"""
    try:
        django.setup()
        print("✅ Django setup completed successfully")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def check_installed_apps():
    """Check if all custom apps are properly configured"""
    from django.conf import settings
    
    expected_apps = ['hotel', 'employees', 'restaurant', 'minibar', 'sms_service']
    installed_apps = settings.INSTALLED_APPS
    
    print("\n📋 Checking installed apps:")
    for app in expected_apps:
        if app in installed_apps:
            print(f"  ✅ {app}")
        else:
            print(f"  ❌ {app} - NOT FOUND")
    
    return all(app in installed_apps for app in expected_apps)

def create_migrations():
    """Create database migrations for all apps"""
    from django.core.management import execute_from_command_line
    
    print("\n🔄 Creating database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Migrations created successfully")
        return True
    except Exception as e:
        print(f"❌ Migration creation failed: {e}")
        return False

def apply_migrations():
    """Apply database migrations"""
    from django.core.management import execute_from_command_line
    
    print("\n🔄 Applying database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Migration application failed: {e}")
        return False

def check_models():
    """Check if models can be imported successfully"""
    print("\n🔍 Checking model imports:")
    
    models_to_check = [
        ('hotel.models', 'Customer'),
        ('employees.models', 'Employee'),
        ('restaurant.models', 'Order'),
        ('minibar.models', 'MinibarProduct'),
        ('sms_service.models', 'SMSMessage'),
    ]
    
    all_good = True
    for module_name, model_name in models_to_check:
        try:
            module = __import__(module_name, fromlist=[model_name])
            model = getattr(module, model_name)
            print(f"  ✅ {module_name}.{model_name}")
        except Exception as e:
            print(f"  ❌ {module_name}.{model_name} - {e}")
            all_good = False
    
    return all_good

def create_superuser():
    """Create a superuser for admin access"""
    from django.contrib.auth.models import User
    
    print("\n👤 Creating superuser...")
    try:
        if User.objects.filter(username='admin').exists():
            print("  ℹ️ Superuser 'admin' already exists")
            return True
        
        User.objects.create_superuser(
            username='admin',
            email='admin@tclussofthotel.com',
            password='admin123'
        )
        print("  ✅ Superuser created successfully")
        print("     Username: admin")
        print("     Password: admin123")
        return True
    except Exception as e:
        print(f"  ❌ Superuser creation failed: {e}")
        return False

def check_redis():
    """Check if Redis is running"""
    print("\n🔄 Checking Redis connection...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("  ✅ Redis is running")
        return True
    except Exception as e:
        print(f"  ❌ Redis connection failed: {e}")
        print("     Please start Redis server: redis-server --daemonize yes")
        return False

def main():
    """Main setup function"""
    print("🏨 Tclussoft Hotel Management System Setup")
    print("=" * 50)
    
    # Step 1: Setup Django
    if not setup_django():
        print("\n❌ Setup failed at Django initialization")
        return False
    
    # Step 2: Check installed apps
    if not check_installed_apps():
        print("\n❌ Setup failed: Missing apps in INSTALLED_APPS")
        return False
    
    # Step 3: Check model imports
    if not check_models():
        print("\n❌ Setup failed: Model import errors")
        return False
    
    # Step 4: Create migrations
    if not create_migrations():
        print("\n❌ Setup failed: Migration creation failed")
        return False
    
    # Step 5: Apply migrations
    if not apply_migrations():
        print("\n❌ Setup failed: Migration application failed")
        return False
    
    # Step 6: Create superuser
    if not create_superuser():
        print("\n❌ Setup failed: Superuser creation failed")
        return False
    
    # Step 7: Check Redis
    redis_ok = check_redis()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Start the Django server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. Login with: admin / admin123")
    
    if redis_ok:
        print("4. Start Celery worker: celery -A tclussoft_hotel worker --loglevel=info")
        print("5. Start Celery beat: celery -A tclussoft_hotel beat --loglevel=info")
    else:
        print("4. Start Redis server first, then Celery services")
    
    return True

if __name__ == '__main__':
    main()