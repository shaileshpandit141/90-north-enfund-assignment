import requests
from django.conf import settings

from utils.base_apiview import BaseAPIView, Response

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class GoogleAuthView(BaseAPIView):
    def get(self, request, *args, **kwargs) -> Response:
        auth_url = (
            "https://accounts.google.com/o/oauth2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            "response_type=code&"
            f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
            "scope="
            + requests.utils.quote(  # type: ignore
                "openid email profile "
                "https://www.googleapis.com/auth/drive "
                "https://www.googleapis.com/auth/drive.file "
                "https://www.googleapis.com/auth/drive.metadata.readonly"
            )
            + "&access_type=offline"
            "&include_granted_scopes=true"
            "&prompt=consent"
        )

        return self.handle_success(
            "Your Sign in request was successful.",
            {
                "auth_url": auth_url,
            },
        )
