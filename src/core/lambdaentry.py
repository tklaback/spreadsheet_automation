import os
from src.core.datastructs import ReviewApiInfo, SpreadsheetInfo
from src.core.appendreviews import append_reviews_to_google_sheets
from google.oauth2.service_account import Credentials
from src.core.tokenmanager import get_review_api_info
import os
from dotenv import load_dotenv
load_dotenv(override=True)

def lambda_handler(event: dict, context: dict) -> dict[str, str|int]:
    try:

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

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
