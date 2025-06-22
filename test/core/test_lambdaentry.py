import pytest
import os
from unittest.mock import Mock
from core.lambda.lambdaentry import lambda_handler


def test_lambda_handler_success(mocker):
    mocker.patch.dict(os.environ, {
        "CREDENTIALS_PATH": "/fake/path.json",
        "SHEET_ID": "spreadsheet123",
        "SHEET_NAME": "Sheet1!A1:E1"
    })

    mock_api_info = Mock()
    mock_review_fn = mocker.patch("src.core.lambdaentry.get_review_api_info", return_value=mock_api_info)
    mocker.patch("src.core.lambdaentry.Credentials.from_service_account_file", return_value=Mock(name="creds"))
    mock_append = mocker.patch("src.core.lambdaentry.append_reviews_to_google_sheets", return_value=None)

    result = lambda_handler(event={}, context={})

    assert result == {"statusCode": 200, "body": ""}
    mock_append.assert_called_once()
    mock_review_fn.assert_called_once()


def test_lambda_handler_missing_sheet_id(mocker):
    mocker.patch.dict(os.environ, {
        "CREDENTIALS_PATH": "/fake/path.json",
        "SHEET_ID": "",
        "SHEET_NAME": "Sheet1!A1:E1"
    })

    mocker.patch("src.core.lambdaentry.get_review_api_info", return_value=mocker.Mock())
    mocker.patch("src.core.lambdaentry.Credentials.from_service_account_file", return_value=mocker.Mock())

    result = lambda_handler(event={}, context={})

    assert result["statusCode"] == 500
    assert result["body"] == "SHEET_ID is a required environment variable"


def test_lambda_handler_append_raises(mocker):
    mocker.patch.dict(os.environ, {
        "CREDENTIALS_PATH": "/fake/path.json",
        "SHEET_ID": "spreadsheet123",
        "SHEET_NAME": "Sheet1!A1:E1"
    })

    mocker.patch("src.core.lambdaentry.get_review_api_info", return_value=mocker.Mock())
    mocker.patch("src.core.lambdaentry.Credentials.from_service_account_file", return_value=mocker.Mock())

    mocker.patch("src.core.lambdaentry.append_reviews_to_google_sheets", side_effect=RuntimeError("Something failed"))

    result = lambda_handler(event={}, context={})

    assert result["statusCode"] == 500
    assert result["body"] == "Something failed"
