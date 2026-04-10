from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/notes/', include('apps.APIs.notes.urls')),
    path('api/cars/', include('apps.APIs.cars.urls')),
]
