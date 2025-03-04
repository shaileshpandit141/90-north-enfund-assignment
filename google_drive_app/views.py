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
