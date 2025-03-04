from django.urls import path

from .views import (
    GoogleDriveFileDetailView,
    GoogleDriveFileListView,
    GoogleDriveFileUploadView,
)

# Base url is "api/v1/google/drive/"
urlpatterns = [
    path("upload/", GoogleDriveFileUploadView.as_view(), name="drive_file_upload"),
    path("list/", GoogleDriveFileListView.as_view(), name="drive_file_list"),
    path(
        "list/<str:file_id>/",
        GoogleDriveFileDetailView.as_view(),
        name="drive_file_detail",
    ),
]
