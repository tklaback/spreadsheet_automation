from typing import List
from datastructs import ReviewApiInfo
from businessreviews import fetch_business_reviews


def append_reviews_to_google_sheets(data: ReviewApiInfo):
    reviews = [review for review in fetch_business_reviews(data)]