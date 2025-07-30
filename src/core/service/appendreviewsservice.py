from src.core.models.datastructs import ReviewApiInfo, SpreadsheetInfo
from src.core.service.fetchreviews import fetch_business_reviews
from src.core.service.networkservice import Network
from src.core.utils.getenvvar import get_required_os_var
import json


def append_reviews_to_google_sheets(
        locations: list[str],
        account_id: str,
        access_token: str,
        ss: SpreadsheetInfo,
        creds
    ):

    location_mapping = json.loads(get_required_os_var("LOCATIONID_TO_DISPLAY_NAME"))

    location_reviews = {}

    for location_id in locations:
        location_name = location_mapping.get(location_id, "Unknown Location")
        if not location_name:
            print(f"Warning: No display name found for location ID {location_id}. Using 'Unknown Location'.")
            location_name = "Unknown Location"
        print(f"Fetching reviews for {location_name} ({location_id})")
        
        reviews = fetch_business_reviews(ReviewApiInfo(account_id, location_id, access_token))
        location_reviews[location_name] = [review.convert_to_list() for review in reviews]

    print("Fetched reviews for all locations")

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    for sheet_name, review_rows in location_reviews.items():
        print(f"Writing {len(review_rows)} reviews to sheet: {sheet_name}")
        
        sheet_range = f"{sheet_name}!A2"

        clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{sheet_range}:Z:clear"
        write_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{sheet_range}"

        Network.build_request(
            {
                "method": "POST",
                "url": clear_url,
                "headers": headers
            }
        )
        print(f"Cleared existing data in sheet: {sheet_name}")

        data = {
            "values": review_rows
        }
        params = {
            "valueInputOption": ss.value_input_option
        }

        Network.build_request(
            {
                "method": "PUT",
                "url": write_url,
                "params": params,
                "headers": headers,
                "data": json.dumps(data)
            }
        )

        print(f"Successfully wrote reviews to sheet: {sheet_name}")

        

