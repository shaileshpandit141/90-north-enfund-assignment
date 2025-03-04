"""URL configuration for app_config project."""

from django.contrib import admin
from django.urls import path, include
from user_auth_app import urls as user_auth_app_urls
from google_drive_app import urls as google_drive_app_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(user_auth_app_urls)),
    path("api/v1/", include(google_drive_app_urls)),
]
