from datastructs import ReviewApiInfo, SpreadsheetInfo
from businessreviews import fetch_business_reviews
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
load_dotenv(override=True)


def append_reviews_to_google_sheets(data: ReviewApiInfo, ss: SpreadsheetInfo):
    reviews = [review.convert_to_list() for review in fetch_business_reviews(data)]

    creds = Credentials.from_service_account_file(
        os.getenv("CREDENTIALS_PATH"))
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)
        values = reviews
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=ss.spreadsheet_id,
                range=ss.range,
                valueInputOption=ss.value_input_option,
                body=body,
            )
            .execute()
        )
        return f"{result.get('updatedCells')} cells updated."
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
