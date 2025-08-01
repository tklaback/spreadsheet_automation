from src.core.utils.getenvvar import get_required_os_var
from src.core.service.authservice import AuthService
from src.core.service.getaccountlocations import get_account, get_locations
from src.core.models.datastructs import SpreadsheetInfo
from src.core.service.appendreviewsservice import append_reviews_to_google_sheets
from src.core.service.sscredsservice import load_credentials

def handler():
    creds = load_credentials()

    auth_service = AuthService.build()

    access_token = auth_service.access_token
    account_id = get_account(access_token)
    locations = get_locations(access_token, account_id)

    
    
    spreadsheet_id = get_required_os_var("SHEET_ID")
    ss = SpreadsheetInfo(spreadsheet_id=spreadsheet_id, value_input_option="USER_ENTERED")
    append_reviews_to_google_sheets(locations, account_id, access_token, ss, creds)
