from dataclasses import dataclass

@dataclass
class ReviewApiInfo:
    account_id: str
    location_id: str
    access_token: str