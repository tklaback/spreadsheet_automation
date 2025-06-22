
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from typing import List
from returns.result import Result, Success, Failure
from src.core.utils.getenvvar import get_required_os_var

def get_locations(spreadsheet_id: str, range_name: str) -> Result[List[List[str]], Error]:

    creds = Credentials.from_service_account_file(
        get_required_os_var("CREDENTIALS_PATH"))
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )

        return Success(result.get("values", []))
    except HttpError as error:
        return Failure(Error())