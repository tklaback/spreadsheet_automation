import requests
from core.dataclasses import ReviewApiInfo
from typing import Generator

def fetch_business_reviews(data: ReviewApiInfo) -> Generator[dict]:
    url = f"https://businessprofile.googleapis.com/v1/{data.account_id}/{data.location_id}/reviews"
    headers = {"Authorization": f"Bearer {data.access_token}"}
    params = {}

    while True:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        page = response.json()

        for review in page.get('reviews', []):
            yield review
        
        token = page.get('pageToken')

        if not token:
            break

        params['pageToken'] = token