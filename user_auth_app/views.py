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


class GoogleCallbackView(BaseAPIView):
    def get(self, request, *args, **kwargs) -> Response:
        code = request.GET.get("code")
        if not code:
            return self.handle_error(
                "Your request was not successful.",
                [
                    {
                        "field": "code",
                        "code": "invalid_code",
                        "message": "Opp's missing code params",
                    }
                ],
            )

        try:
            google_payload = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            google_response = requests.post(GOOGLE_TOKEN_URL, data=google_payload)
            tokens = google_response.json()
            headers = {"Authorization": f"Bearer {tokens.get('access_token')}"}
            user_info = requests.get(GOOGLE_USER_INFO_URL, headers=headers).json()

            return self.handle_success(
                "Sign in request was successful",
                {
                    "user": user_info,
                    "tokens": tokens,
                },
            )
        except Exception as error:
            return self.handle_error(
                "Your request was not successful.",
                [
                    {
                        "field": "none",
                        "code": "google_callback",
                        "message": str(error),
                    }
                ],
            )
