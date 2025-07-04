"""boutique_ado URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.http import HttpResponse

def ignore_well_known_request(request):
    return HttpResponse(status=204)  # or 404 with empty body


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('.well-known/appspecific/com.chrome.devtools.json', ignore_well_known_request), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
