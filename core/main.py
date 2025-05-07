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

@dataclass
class Review:
    author: str
    rating: int
    time: str
    text: str

load_dotenv(override=True)

def get_locations(spreadsheet_id: str, range_name: str) -> List[List[str]]:

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

        return result.get("values", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_reviews(place_id: str) -> List[Review]:
    api_key = os.getenv("API_KEY")
    review_url = f"https://places.googleapis.com/v1/places/{place_id}?fields=reviews&key={api_key}"

    try:
        response = requests.get(review_url)
        response.raise_for_status()

        data = response.json()

    except ConnectionError as ce:
        print(f"Connection Error occurred while getting review data: {ce}")
        return []
    except RHTTPError as he:
        print(f"HTTPError occurred while getting review data: {he}")
        return []
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return []
       
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

    return list_of_reviews

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
#   get_locations(os.getenv("SHEET_ID"), "'Settings'!A2:B6")
    get_reviews("ChIJHe7281r1UocRbjHXIVdRMcE")