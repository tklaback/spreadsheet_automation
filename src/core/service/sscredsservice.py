from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from core.utils.getenvvar import get_required_os_var
import json
import base64

def load_credentials():
    encoded = get_required_os_var("GOOGLE_CREDENTIALS_BASE64")
    decoded = base64.b64decode(encoded).decode("utf-8")

    service_account_info = json.loads(decoded)

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    credentials.refresh(Request())
    return credentials