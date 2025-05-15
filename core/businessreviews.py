import requests
from core.datastructs import ReviewApiInfo
from typing import Generator
from datastructs import Review
from constants import RATING_MAPPING

def fetch_business_reviews(data: ReviewApiInfo) -> Generator[Review]:
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