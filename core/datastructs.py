from dataclasses import dataclass

@dataclass
class ReviewApiInfo:
    account_id: str
    location_id: str
    access_token: str

@dataclass
class Review:
    id: str
    author: str
    rating: int
    time: str
    comment: str