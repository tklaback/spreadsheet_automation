from core.models.datastructs import ReviewApiInfo, SpreadsheetInfo
from core.service.fetchreviews import fetch_business_reviews
from core.service.networkservice import Network


def append_reviews_to_google_sheets(
        locations: list[str],
        account_id: str,
        access_token: str,
        ss: SpreadsheetInfo,
        creds
    ):

    reviews = [
        review.convert_to_list()
        for location_id in locations
        for review in fetch_business_reviews(ReviewApiInfo(account_id, location_id, access_token))
    ]


    url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{ss.range}"
    clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ss.spreadsheet_id}/values/{ss.range}:Z:clear"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    Network.build_request(
        {
            "method": "POST",
            "url": clear_url,
            "headers": headers
        }
    )

    data = {
        "values": reviews
    }
    params = {
        "valueInputOption": ss.value_input_option
    }
    response = Network.build_request(
        {
            "method": "PUT",
            "url": url, 
            "headers": headers, 
            "params": params,
            "json": data
        }
    )

    return response.json()
        
