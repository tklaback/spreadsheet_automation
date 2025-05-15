# test_reviews.py

import pytest
import requests
from src.core.datastructs import Review
from types import SimpleNamespace
from src.core.businessreviews import fetch_business_reviews


@pytest.fixture
def api_info():
    return SimpleNamespace(
        account_id="accounts/123456",
        location_id="locations/7890",
        access_token="fake-token"
    )

def test_fetch_reviews_pagination(mocker, api_info):
    first_page = {
        "reviews": [
            {
                "reviewId": "r1",
                "reviewer": {"displayName": "Alice"},
                "starRating": "FIVE",
                "createTime": "2023-01-01T00:00:00Z",
                "comment": "Great!"
            }
        ],
        "pageToken": "next-page-token"
    }
    second_page = {
        "reviews": [
            {
                "reviewId": "r2",
                "reviewer": {"displayName": "Bob"},
                "starRating": "FOUR",
                "createTime": "2023-01-02T00:00:00Z",
                "comment": "Good!"
            }
        ]
    }

    mock_get = mocker.patch("src.core.businessreviews.requests.get", side_effect=[
        mocker.Mock(json=lambda: first_page, raise_for_status=lambda: None),
        mocker.Mock(json=lambda: second_page, raise_for_status=lambda: None),
    ])

    expected_reviews = [
        Review("r1", "Alice", 5, "2023-01-01T00:00:00Z", "Great!"),
        Review("r2", "Bob", 4, "2023-01-02T00:00:00Z", "Good!")
    ]

    results = list(fetch_business_reviews(api_info))

    assert results == expected_reviews
    assert mock_get.call_count == 2

def test_fetch_reviews_http_error(mocker, api_info):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("403 Forbidden")
    mocker.patch("src.core.businessreviews.requests.get", return_value=mock_response)

    with pytest.raises(requests.HTTPError, match="403 Forbidden"):
        list(fetch_business_reviews(api_info))

def test_fetch_reviews_missing_data(mocker, api_info):
    malformed_page = {
        "reviews": [
            {
                "reviewId": "r1",
                # missing reviewer, starRating, etc.
            }
        ]
    }
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = malformed_page

    mocker.patch("src.core.businessreviews.requests.get", return_value=mock_response)

    with pytest.raises(KeyError):
        list(fetch_business_reviews(api_info))
