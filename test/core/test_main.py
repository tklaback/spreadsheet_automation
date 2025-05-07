from core.main import get_values

# def get_values(spreadsheet_id: str, range_name: str) -> List[List[str]]:

#     creds = Credentials.from_service_account_file(
#         os.getenv("CREDENTIALS_PATH"))
#     try:
#         service = build("sheets", "v4", credentials=creds)

#         result = (
#             service.spreadsheets()
#             .values()
#             .get(spreadsheetId=spreadsheet_id, range=range_name)
#             .execute()
#         )

#         return result.get("values", [])
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error

def test_get_values(mocker):
    mock_service_account_file = mocker.patch("core.main.Credentials.from_service_account_file", return_value="creds")
    mocker.patch("core.main.os.getenv", return_value="secret_title")

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


