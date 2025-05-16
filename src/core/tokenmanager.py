import json
import boto3 # type: ignore
import boto3.session
from botocore.exceptions import ClientError
import requests
from src.core.datastructs import ReviewApiInfo, SpreadsheetInfo
from google.oauth2.service_account import Credentials

# Secrets Manager helper
def get_google_secrets(secret_name: str, region_name: str) -> dict[str, str]:
    """
    Expects an AWS Secrets Manager secret whose SecretString is JSON with keys:
      {
        "client_id": "...",
        "client_secret": "...",
        "refresh_token": "...",
        "account_id": "...",
        "location_id": "..."
      }
    """

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response['SecretString'])

def refresh_access_token(client_id: str, client_secret: str, refresh_token: str):
    """
    Exchanges a refresh_token for a new access_token.
    """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id":     client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type":    "refresh_token",
    }
    r = requests.post(token_url, data=payload)
    r.raise_for_status()
    return r.json()["access_token"]

def get_review_api_info(google_secret_name: str, region_name: str) -> ReviewApiInfo:
    secrets = get_google_secrets(google_secret_name, region_name)
    assert isinstance(secrets, dict)

    client_id     = secrets["client_id"]
    client_secret = secrets["client_secret"]
    refresh_token = secrets["refresh_token"]
    account_id    = secrets["account_id"]
    location_id   = secrets["location_id"]

    access_token = refresh_access_token(client_id, client_secret, refresh_token)

    return ReviewApiInfo(
        account_id=account_id,
        location_id=location_id,
        access_token=access_token
    )
