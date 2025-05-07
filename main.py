import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

def get_values(spreadsheet_id, range_name):
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("CREDENTIALS_PATH"))

    service = build('sheets', 'v4', credentials=creds)

    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_reviews():
   pass

def update_values(spreadsheet_id, range_name, value_input_option, _values):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    values = _values
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


# if __name__ == "__main__":
#   # Pass: spreadsheet_id,  range_name, value_input_option and  _values
#   update_values(
#       os.getenv("SHEET_ID"),
#       "A1:C2",
#       "USER_ENTERED",
#       [["A", "B"], ["C", "D"]],
#   )

if __name__ == "__main__":
  # Pass: spreadsheet_id, and range_name
  get_values(os.getenv("SHEET_ID"), "'Settings'!A2:B6")
