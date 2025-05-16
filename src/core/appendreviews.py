from src.core.datastructs import ReviewApiInfo, SpreadsheetInfo
from src.core.businessreviews import fetch_business_reviews
import requests


def append_reviews_to_google_sheets(api_info: ReviewApiInfo, ss: SpreadsheetInfo, creds):
    reviews = [review.convert_to_list() for review in fetch_business_reviews(api_info)]

    # pylint: disable=maybe-no-member
    try:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{ss.range}"
        clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{ss.range}:Z:clear"
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }

        clear_response = requests.post(clear_url, headers=headers)
        clear_response.raise_for_status()

        data = {
            "values": reviews
        }
        params = {
            "valueInputOption": ss.value_input_option
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as error:
        print(f"An error occurred: {error}")
        raise error
