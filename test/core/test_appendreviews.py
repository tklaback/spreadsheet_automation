import pytest
from googleapiclient.errors import HttpError
from types import SimpleNamespace
from src.core.appendreviews import append_reviews_to_google_sheets


@pytest.fixture
def api_info():
    return SimpleNamespace(
        account_id="accounts/123456",
        location_id="locations/7890",
        access_token="fake-token"
    )

@pytest.fixture
def spreadsheet_info():
    return SimpleNamespace(
        spreadsheet_id="sheet123",
        range="Sheet1!A1:E1",
        value_input_option="RAW"
    )

@pytest.fixture
def creds(mocker):
    return mocker.Mock(name="credentials")


def test_append_reviews_success(mocker, api_info, spreadsheet_info, creds):
    # Mock a review object with .convert_to_list()
    mock_review = mocker.Mock()
    mock_review.convert_to_list.return_value = ["r1", "Alice", 5, "2023-01-01", "Great!"]

    # Mock fetch_business_reviews to return our mock review
    mocker.patch("src.core.appendreviews.fetch_business_reviews", return_value=[mock_review])

    # Mock Google Sheets API chain: build(...).spreadsheets().values().append(...).execute()
    mock_service = mocker.Mock()
    mock_values = mock_service.spreadsheets.return_value.values.return_value
    mock_values.append.return_value.execute.return_value = {"updatedCells": 5}

    mocker.patch("src.core.appendreviews.build", return_value=mock_service)

    result = append_reviews_to_google_sheets(api_info, spreadsheet_info, creds)
    assert result == "5 cells updated."

def test_append_reviews_http_error(mocker, api_info, spreadsheet_info, creds):
    # Empty review list for simplicity
    mocker.patch("src.core.appendreviews.fetch_business_reviews", return_value=[])

    # Simulate HttpError on append().execute()
    mock_service = mocker.Mock()
    mock_values = mock_service.spreadsheets.return_value.values.return_value
    mock_values.append.return_value.execute.side_effect = HttpError(
        resp=mocker.Mock(status=403), content=b"Permission denied"
    )

    mocker.patch("src.core.appendreviews.build", return_value=mock_service)

    with pytest.raises(HttpError) as e:
        append_reviews_to_google_sheets(api_info, spreadsheet_info, creds)
