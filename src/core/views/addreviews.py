from core.models.datastructs import ReviewApiInfo, SpreadsheetInfo
from core.service.appendreviewsservice import append_reviews_to_google_sheets
from google.oauth2.service_account import Credentials
from src.core.tokenmanager import get_review_api_info
from google.auth.transport.requests import Request
import os



def entry(event: dict, context: dict) -> dict[str, str|int]:
    try:
        secret_name = get_required_os_var("GOOGLE_SECRET_NAME")
        # creds = load_credentials()
        
        # spreadsheet_id = get_required_os_var("SHEET_ID")
        # range = get_required_os_var("SHEET_NAME")
        # ss = SpreadsheetInfo(spreadsheet_id=spreadsheet_id, range=range, value_input_option="USER_ENTERED")
        # append_reviews_to_google_sheets(api_info, ss, creds)

        return {
            "statusCode": 200,
            "body": ""
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
