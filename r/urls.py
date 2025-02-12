"""
URL configuration for r project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from r.views import  contact, expand_gmap_url, home, mysearch, nearby_properties, property_search, service, test_map

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', home, name='home'),
    path('service/', service, name='service'),
    path('contact/', contact, name='contact'),
    path("expand-url/", expand_gmap_url, name="expand_gmap_url"),
    path('nearby/', nearby_properties, name='nearby_properties'),
    path("test-map/", test_map, name="test_map"),
    path('search/', property_search, name='property_search'),
    path('mysearch/', mysearch, name='mysearch'),

    path('', include('account.urls')),
    path('', include('property.urls')),
    path('api/', include('api.urls')),
    path('chat/', include('chat.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)