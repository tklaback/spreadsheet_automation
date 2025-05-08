import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from typing import List
from dataclasses import dataclass
import requests
from requests import HTTPError as RHTTPError, ConnectionError
import os
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful
from returns.functions import not_

load_dotenv(override=True)

SETTINGS_SHEET_NAME = "Settings"
LOCATIONS_RANGE = "A2:B6"

class Error:
    def get_message():
        pass

@dataclass
class Review:
    author: str
    rating: int
    time: str
    text: str


def get_locations(spreadsheet_id: str, range_name: str) -> Result[List[List[str]], Error]:

    creds = Credentials.from_service_account_file(
        os.getenv("CREDENTIALS_PATH"))
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


def get_reviews(place_id: str) -> Result[List[Review], Error]:
    review_url = f"https://places.googleapis.com/v1/places/{place_id}?fields=reviews&key={os.getenv("API_KEY")}"

    try:
        response = requests.get(review_url)
        response.raise_for_status()

        data = response.json()

    except ConnectionError as ce:
        print(f"Connection Error occurred while getting review data: {ce}")
        return Failure(Error())
    except RHTTPError as he:
        print(f"HTTPError occurred while getting review data: {he}")
        return Failure(Error())
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return Failure(Error())
       
    raw_reviews = data.get('reviews', [])

    list_of_reviews = [
        Review(
            author=review.get('authorAttribution', {}).get('displayName'),
            rating=int(review.get('rating')),
            time=review.get('publishTime'),
            text=review.get('text', {}).get('text')
        )
        for review in raw_reviews
    ]

    return Success(list_of_reviews)

def update_values(spreadsheet_id, range_name, value_input_option, _values) -> Result[str, Error]:
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = Credentials.from_service_account_file(
        os.getenv("CREDENTIALS_PATH"))
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)
        values = _values
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range="Sheet1",
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        Success(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return Failure(Error())

# if __name__ == "__main__":
#   # Pass: spreadsheet_id,  range_name, value_input_option and  _values
#   update_values(
#       os.getenv("SHEET_ID"),
#       "A1:C2",
#       "USER_ENTERED",
#       [["A", "B"], ["C", "D"]],
#   )

# if __name__ == "__main__":
# #   Pass: spreadsheet_id, and range_name
# #   get_locations(os.getenv("SHEET_ID"), "'Settings'!A2:B6")
#     get_reviews("ChIJHe7281r1UocRbjHXIVdRMcE")

def main():
    # 1) get locations
    # 2) get reviews for each location
    # 3) for each location, write the reviews

    locations_result = get_locations(os.getenv("SHEET_ID"), f"'{SETTINGS_SHEET_NAME}'!{LOCATIONS_RANGE}")
    if not_(is_successful)(locations_result):
        print(locations_result.failure().get_message())
        return

    locations = locations_result.unwrap()

    print(f"Grabbed {len(locations)} locations")

main()