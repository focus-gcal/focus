from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import config
import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

User = get_user_model()


@dataclass
class GoogleCredentials:
    id_token: Optional[str]
    access_token: str
    refresh_token: Optional[str]
    expiry: datetime
    scopes: List[str]


@dataclass
class GoogleUserInfo:
    sub: str
    email: str
    name: str


class GoogleAuthService:
    client_id = config.OAUTH["CLIENT_ID"]
    client_secret = config.OAUTH["CLIENT_SECRET"]
    redirect_uri = config.OAUTH["REDIRECT_URI"]
    token_url = "https://oauth2.googleapis.com/token"
    auth_uri = "https://accounts.google.com/o/oauth2/v2/auth"
    scopes = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/calendar",
    ]

    @staticmethod
    def exchange_code_for_token(code: str):
        try:
            flow = Flow.from_client_config(
                client_config={
                    "web": {
                        "client_id": GoogleAuthService.client_id,
                        "client_secret": GoogleAuthService.client_secret,
                        "auth_uri": GoogleAuthService.auth_uri,
                        "token_uri": GoogleAuthService.token_url,
                        "redirect_uris": [GoogleAuthService.redirect_uri],
                    }
                },
                scopes=GoogleAuthService.scopes,
                redirect_uri=GoogleAuthService.redirect_uri,
            )
            flow.fetch_token(code=code)
            creds = flow.credentials
            creds.expiry = creds.expiry.replace(tzinfo=timezone.utc)
            if not creds.expiry or creds.expiry < datetime.now(timezone.utc):
                return None, "Token expired"
            if not set(GoogleAuthService.scopes).issubset(set(creds.scopes or [])):
                return None, "Invalid scopes"
            return (
                GoogleCredentials(
                    id_token=creds.id_token,
                    access_token=creds.token,
                    refresh_token=creds.refresh_token,
                    expiry=creds.expiry,
                    scopes=creds.scopes if creds.scopes else [],
                ),
                None,
            )
        except Exception as e:
            print(e)
            return None, None

    @staticmethod
    def get_user_info(id_token: str):
        try:
            request = google_requests.Request()

            claims = google_id_token.verify_oauth2_token(
                id_token,
                request,
                audience=GoogleAuthService.client_id,
            )

            if claims["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Invalid issuer")
            if claims["email_verified"] is False:
                raise ValueError("Email not verified by Google")

            return GoogleUserInfo(
                sub=claims["sub"],
                email=claims["email"],
                name=claims["name"],
            )

        except Exception as e:
            print("Invalid Google ID token:", e)
            return None

    @staticmethod
    def store_access_token(user_id: int, credentials: GoogleCredentials):
        redis_key = f"google_access_token_{user_id}"
        now = datetime.now(timezone.utc)
        if not credentials.expiry:
            return
        expires_in = int((credentials.expiry - now).total_seconds())
        expires_in = max(expires_in - 60, 0)

        cache.set(redis_key, credentials.access_token, timeout=expires_in)

    @staticmethod
    def refresh_access_token(refresh_token: str) -> GoogleCredentials | None:
        try:
            creds = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri=GoogleAuthService.token_url,
                client_id=GoogleAuthService.client_id,
                client_secret=GoogleAuthService.client_secret,
            )

            request = google_requests.Request()
            creds.refresh(request)
            if creds.expiry and creds.expiry.tzinfo is None:
                creds.expiry = creds.expiry.replace(tzinfo=timezone.utc)

            return GoogleCredentials(
                id_token=None,
                access_token=creds.token,
                refresh_token=creds.refresh_token,
                expiry=creds.expiry,
                scopes=creds.scopes if creds.scopes else [],
            )
        except Exception:
            return None

    @staticmethod
    def get_access_token(user_id: int):
        redis_key = f"google_access_token_{user_id}"
        return cache.get(redis_key)

    @staticmethod
    def test_access_token(access_token: str) -> bool:
        try:
            resp = requests.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"access_token": access_token},
                timeout=10,
            )
        except Exception:
            return False
        return resp.status_code == 200

    @staticmethod
    def get_valid_access_token(user_id: int):
        access_token = GoogleAuthService.get_access_token(user_id)
        if access_token and GoogleAuthService.test_access_token(access_token):
            return access_token
        refresh_token = User.objects.get(id=user_id).refresh_token
        if not refresh_token:
            return None
        new_access_token = GoogleAuthService.refresh_access_token(refresh_token)
        if not new_access_token:
            return None
        GoogleAuthService.store_access_token(user_id, new_access_token)
        return new_access_token.access_token
