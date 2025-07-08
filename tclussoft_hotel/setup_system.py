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
    
    print("\n✅ Basic setup checks passed!")
    print("Now try running: python manage.py makemigrations")
    return True

if __name__ == '__main__':
    main()
