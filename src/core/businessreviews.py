import requests
from src.core.datastructs import ReviewApiInfo, Review
from typing import Iterable
from src.core.constants import RATING_MAPPING

def fetch_business_reviews(api_info: ReviewApiInfo) -> Iterable[Review]:
    url = f"https://businessprofile.googleapis.com/v1/{api_info.account_id}/{api_info.location_id}/reviews"
    headers = {"Authorization": f"Bearer {api_info.access_token}"}
    params = {}

    while True:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        page = response.json()

        for review_data in page.get('reviews', []):
            review = Review(
                id=review_data['reviewId'],
                author=review_data['reviewer']['displayName'],
                rating=RATING_MAPPING[review_data['starRating']],
                time=review_data['createTime'],
                comment=review_data['comment']
            )
            yield review
        
        token = page.get('pageToken')

        if not token:
            break

        params['pageToken'] = token