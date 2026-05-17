from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/routing/', include('routing.urls')),
]
