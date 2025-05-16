from src.core.datastructs import ReviewApiInfo, SpreadsheetInfo
from src.core.appendreviews import append_reviews_to_google_sheets
from google.oauth2.service_account import Credentials
from src.core.tokenmanager import get_review_api_info
from google.auth.transport.requests import Request
import boto3
import json
import os

def load_credentials():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=get_required_os_var("SECRET_ID"))
    credentials_dict = json.loads(response['SecretString'])

    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    credentials.refresh(Request())
    return credentials

def get_required_os_var(env_var_name: str) -> str:
    value = os.environ.get(env_var_name)

    assert value, f"{value} is a required environment variable"

    return value

def lambda_handler(event: dict, context: dict) -> dict[str, str|int]:
    try:
        secret_name = get_required_os_var("GOOGLE_SECRET_NAME")
        region_name = os.environ.get("AWS_REGION", "us-east-1")

        api_info: ReviewApiInfo = get_review_api_info(secret_name, region_name)

        os.environ.get("")
        creds = load_credentials()
        
        spreadsheet_id = get_required_os_var("SHEET_ID")

        range = get_required_os_var("SHEET_NAME")

        ss = SpreadsheetInfo(spreadsheet_id=spreadsheet_id, range=range, value_input_option="USER_ENTERED")
        append_reviews_to_google_sheets(api_info, ss, creds)

        return {
            "statusCode": 200,
            "body": ""
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
