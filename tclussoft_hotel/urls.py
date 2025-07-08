"""
URL configuration for tclussoft_hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.http import HttpResponse

def home_view(request):
    """Temporary home view - redirect to admin until frontend is built"""
    if request.user.is_authenticated:
        return redirect('/admin/')
    else:
        return redirect('/admin/login/')

def health_check(request):
    """Health check endpoint"""
    return HttpResponse("OK")

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Home page
    path('', home_view, name='home'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API endpoints (when views are created)
    path('api/hotel/', include('hotel_management.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/restaurant/', include('restaurant.urls')),
    path('api/minibar/', include('minibar.urls')),
    path('api/sms/', include('sms_service.urls')),
    
    # Health check
    path('health/', health_check, name='health_check'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
