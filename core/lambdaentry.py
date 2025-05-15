import os
from core.datastructs import ReviewApiInfo, SpreadsheetInfo
from appendreviews import append_reviews_to_google_sheets
from google.oauth2.service_account import Credentials
from tokenmanager import get_review_api_info
import os
from dotenv import load_dotenv
load_dotenv(override=True)

def lambda_handler(event: str, context: str) -> dict[str, str|int]:
    api_info: ReviewApiInfo = get_review_api_info()

    creds = Credentials.from_service_account_file(
        os.getenv("CREDENTIALS_PATH"))
    
    spreadsheet_id = os.getenv("SHEET_ID")
    assert spreadsheet_id, "SHEET_ID is a required environment variable"

    range = os.getenv("SHEET_NAME")
    assert range, "SHEET_NAME is a required environment variable"

    ss = SpreadsheetInfo(spreadsheet_id=spreadsheet_id, range=range, value_input_option="USER_ENTERED")
    append_reviews_to_google_sheets(api_info, ss, creds)


    return {
        "statusCode": 200,
        "body": ""
    }