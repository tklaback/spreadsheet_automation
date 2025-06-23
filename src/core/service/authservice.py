import os
import time
from dataclasses import dataclass
from dotenv import load_dotenv
from core.service.networkservice import Network
from core.utils.getenvvar import get_required_os_var

load_dotenv()

@dataclass
class AuthService:
    access_token: str
    token_type: str
    expire_time: int
    scope: str

    __instance = None

    def is_expired(self) -> bool:
        return int(time.time()) >= self.expire_time

    @staticmethod
    def build() -> "AuthService":
        """
        Exchanges a refresh_token for a new access_token.
        """
        if AuthService.__instance and not AuthService.__instance.is_expired():
            return AuthService.__instance

        client_id = get_required_os_var("CLIENT_ID")
        client_secret = get_required_os_var("CLIENT_SECRET")
        refresh_token = get_required_os_var("REFRESH_TOKEN")

        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id":     client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type":    "refresh_token",
        }
        r = Network.build_request(
            {
                "method": "POST",
                "url": token_url,
                "data": payload
            }
        )

        data = r.json()

        now_secs = int(time.time())
        expire_time = now_secs + int(data["expires_in"])

        print("Successfully obtained access token")

        AuthService.__instance = AuthService(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expire_time=expire_time,
            scope=data["scope"]
        )

        return AuthService.__instance