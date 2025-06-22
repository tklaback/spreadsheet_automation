from core.utils.getenvvar import get_required_os_var
from core.service.authservice import AuthService

def handler(event: dict, context: dict) -> dict[str, str|int]:
    try:
        # creds = load_credentials()

        AuthService.build(["https://www.googleapis.com/auth/business.manage"])
        
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
