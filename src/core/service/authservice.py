import os
import time
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import ClassVar

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
    def build(scopes: list[str]) -> "AuthService":
        if AuthService.__instance and not AuthService.__instance.is_expired():
            return AuthService.__instance

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Uber Client ID and Client Secret must be set in environment variables.")

        if not isinstance(scopes, list) or not scopes:
            raise ValueError("Scopes must be a non-empty list.")

        form = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": " ".join(scopes),
        }

        try:
            response = requests.post("https://accounts.google.com/o/oauth2/v2/auth", data=form)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print("Failed to obtain access token:", e)
            raise

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