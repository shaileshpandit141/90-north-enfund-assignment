from django.urls import path

from .views import GoogleAuthView, GoogleCallbackView

# Base url is "api/v1/auth/"
urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="google_auth"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google_auth_callback"),
]
