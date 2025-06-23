from core.models.datastructs import ReviewApiInfo, SpreadsheetInfo
from core.service.fetchreviews import fetch_business_reviews
from core.service.networkservice import Network


def append_reviews_to_google_sheets(api_info: ReviewApiInfo, ss: SpreadsheetInfo, creds):
    reviews = [review.convert_to_list() for review in fetch_business_reviews(api_info)]

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
            "method": "POST",
            "url": url, 
            "headers":headers, 
            "params":params,
            "json":data
        }
    )
    response.raise_for_status()
    return response.json()
        
