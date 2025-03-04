from typing import Any, Dict, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from rest_framework.parsers import MultiPartParser

from utils.base_apiview import BaseAPIView, Response


class GoogleDriveFileListView(BaseAPIView):
    def get(self, request) -> Response:
        """Fetch files from Google Drive using an access token."""
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                raise Exception("Missing access token")

            # Initialize credentials with only the access token
            credentials = Credentials(token=access_token.replace("Bearer ", ""))

            drive_service = build("drive", "v3", credentials=credentials)

            # Fetch files with id, name, and mimeType (media type)
            files: List[Dict[str, Any]] = (
                drive_service.files()
                .list(
                    fields="files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink, webContentLink)"
                )
                .execute()
                .get("files", [])
            )

            return self.handle_success("File list request was successful.", files)
        except Exception as error:
            return self.handle_error(
                "File list request was not successful.",
                [
                    {
                        "field": "none",
                        "code": "google_drive",
                        "message": (
                            error.get("message", "Invalid request")
                            if isinstance(error, dict)
                            else str(error)
                        ),
                    }
                ],
            )


class GoogleDriveFileDetailView(BaseAPIView):
    def get(self, request, file_id: str) -> Response:
        """Fetch details of a specific file from Google Drive, including a viewable link."""
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                raise Exception("Missing access token")

            # Initialize credentials
            credentials = Credentials(token=access_token.replace("Bearer ", ""))

            drive_service = build("drive", "v3", credentials=credentials)

            # Fetch file details, including URLs
            file_metadata: Dict[str, Any] = (
                drive_service.files()
                .get(
                    fileId=file_id,
                    fields="id, name, mimeType, size, createdTime, modifiedTime, webViewLink, webContentLink",
                )
                .execute()
            )

            return self.handle_success(
                "File details fetched successfully.", file_metadata
            )
        except Exception as error:
            return self.handle_error(
                "File details request failed.",
                [
                    {
                        "field": "none",
                        "code": "google_drive",
                        "message": str(error),
                    }
                ],
            )


class GoogleDriveFileUploadView(BaseAPIView):
    parser_classes = [MultiPartParser]

    def post(self, request) -> Response:
        """Upload a file to Google Drive using an access token."""
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                raise Exception("Missing access token")

            file_obj = request.FILES.get("file")
            if not file_obj:
                raise Exception("No file provided")

            credentials = Credentials(token=access_token.replace("Bearer ", ""))
            drive_service = build("drive", "v3", credentials=credentials)

            # Upload file metadata
            file_metadata = {"name": file_obj.name}

            media = MediaIoBaseUpload(
                file_obj, mimetype=file_obj.content_type, resumable=True
            )

            uploaded_file = (
                drive_service.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    fields="id, name, webViewLink, webContentLink",
                )
                .execute()
            )

            return self.handle_success("File uploaded successfully.", uploaded_file)
        except Exception as error:
            return self.handle_error(
                "File upload failed.",
                [
                    {
                        "field": "none",
                        "code": "google_drive",
                        "message": str(error),
                    }
                ],
            )
