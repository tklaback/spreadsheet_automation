import requests
from core.dataclasses import ReviewApiInfo

def fetch_business_reviews(data: ReviewApiInfo) -> str:
    """
    Calls the Google Business Profile API to list reviews.
    """
    url = f"https://businessprofile.googleapis.com/v1/{data.account_id}/{data.location_id}/reviews"
    headers = {"Authorization": f"Bearer {data.access_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()