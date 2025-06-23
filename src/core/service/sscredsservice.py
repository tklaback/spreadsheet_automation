from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from core.utils.getenvvar import get_required_os_var
import json

def load_credentials():
    credentials_dict = json.loads(get_required_os_var("SERVICE_ACC_CREDS"))

    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    credentials.refresh(Request())
    return credentials