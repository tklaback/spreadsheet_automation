from core.main import get_values
from googleapiclient.errors import HttpError
import pytest

# def get_values(spreadsheet_id: str, range_name: str) -> List[List[str]]:

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error

@pytest.fixture
def mock_credentials_service_account_file(mocker):
    return mocker.patch("core.main.Credentials.from_service_account_file", return_value="creds")

@pytest.fixture
def mock_os(mocker):
    mocker.patch("core.main.os.getenv", return_value="secret_title")

def test_get_values_success(mock_os, mock_credentials_service_account_file, mocker):
    mock_service_account_file = mock_credentials_service_account_file
    mock_os

    mock_service = mocker.Mock()
    mock_spreadsheets = mocker.Mock()
    mock_values = mocker.Mock()
    mock_request = mocker.Mock()

    mock_request.execute.return_value = {"values": [["location1_name", "location1_id"], ["location2_name", "location3_id"]]}
    mock_values.get.return_value        = mock_request
    mock_spreadsheets.values.return_value = mock_values
    mock_service.spreadsheets.return_value = mock_spreadsheets

    mock_build = mocker.patch("core.main.build", return_value=mock_service)
    response = get_values("spreadsheet_id", "spread_sheet_name")

    mock_service_account_file.assert_called_once_with("secret_title")
    mock_build.assert_called_once_with("sheets", "v4", credentials="creds")
    assert response == [["location1_name", "location1_id"], ["location2_name", "location3_id"]]


# def test_get_values_failure(mock_os, mock_credentials_service_account_file, mocker):
#     mock_service_account_file = mock_credentials_service_account_file
#     mock_os

#     def bad_execute():
#         raise HttpError(resp=mocker.Mock(status=404), content=b"Not found")

#     fake_service = mocker.Mock()
#     mock_build = mocker.patch("core.main.build", return_value=fake_service)
#     fake_service.spreadsheets.return_value.values.return_value.get.return_value.execute = bad_execute

#     with pytest.raises(HttpError) as e:
#         result = get_values("id", "range")