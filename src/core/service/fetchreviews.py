from src.core.models.datastructs import ReviewApiInfo, Review
from typing import Iterable
from src.core.utils.constants import RATING_MAPPING
from src.core.service.networkservice import Network

def fetch_business_reviews(api_info: ReviewApiInfo) -> Iterable[Review]:
    url = f"https://mybusiness.googleapis.com/v4/accounts/{api_info.account_id}/locations/{api_info.location_id}/reviews"
    headers = {"Authorization": f"Bearer {api_info.access_token}"}
    params = {}

    while True:

        response = Network.build_request(
            {
                "method": "GET",
                "url": url,
                "headers": headers,
                "params": params
            }
        )
        page = response.json()

        print("Retrieved page of reviews")

        for review_data in page.get('reviews', []):
            review = Review(
                id=review_data.get('reviewId', 'n/a'),
                author=review_data.get('reviewer', {}).get('displayName', 'n/a'),
                rating=RATING_MAPPING[review_data.get('starRating', 'n/a')],
                time=review_data.get('createTime', 'n/a'),
                comment=review_data.get('comment', 'n/a')
            )
            yield review
        
        token = page.get('nextPageToken')

        if not token:
            break

        params['pageToken'] = token