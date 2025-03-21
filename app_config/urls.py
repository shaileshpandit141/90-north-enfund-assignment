"""URL configuration for app_config project."""

from django.contrib import admin
from django.urls import include, path

from google_drive_app import urls as google_drive_app_urls
from user_auth_app import urls as user_auth_app_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include(user_auth_app_urls)),
    path("api/v1/google/drive/", include(google_drive_app_urls)),
]
