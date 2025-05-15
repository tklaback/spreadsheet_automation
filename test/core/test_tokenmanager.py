import os
import json
import pytest
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError
from src.core.tokenmanager import get_google_secrets, refresh_access_token
import requests

@mock_aws
def test_get_google_secrets_success():
    secret_payload = {
        "client_id": "abc123",
        "client_secret": "shh-its-secret",
        "refresh_token": "rt-xyz",
        "account_id": "accounts/111",
        "location_id": "locations/222"
    }

    region = "us-west-2"
    secret_name = "MyTestSecret"

    os.environ["GOOGLE_SECRET_NAME"] = secret_name
    os.environ["AWS_REGION"] = region

    client = boto3.client("secretsmanager", region_name=region)
    client.create_secret(
        Name=secret_name,
        SecretString=json.dumps(secret_payload)
    )

    result = get_google_secrets()

    assert isinstance(result, dict)
    assert result == secret_payload


def test_get_google_secrets_success_with_client_error(mocker):
    secret_payload = {
        "client_id": "abc123",
        "client_secret": "shh-its-secret",
        "refresh_token": "rt-xyz",
        "account_id": "accounts/111",
        "location_id": "locations/222"
    }

    region = "us-west-2"
    secret_name = "MyTestSecret"

    os.environ["GOOGLE_SECRET_NAME"] = secret_name
    os.environ["AWS_REGION"] = region

    mock_session = mocker.Mock()
    mock_client = mocker.Mock()
    error = ClientError(mocker.MagicMock(), mocker.MagicMock())
    mocker.patch("src.core.tokenmanager.boto3.session.Session", return_value=mock_session)
    mock_session.client.return_value = mock_client
    mock_client.get_secret_value.side_effect = error

    with pytest.raises(ClientError) as e:
        get_google_secrets()

def test_refresh_access_token_success(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"access_token": "new-token-123"}

    mock_post = mocker.patch("src.core.tokenmanager.requests.post", return_value=mock_response)

    token = refresh_access_token("client-id", "client-secret", "refresh-token")

    assert token == "new-token-123"
    mock_post.assert_called_once_with(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": "client-id",
            "client_secret": "client-secret",
            "refresh_token": "refresh-token",
            "grant_type": "refresh_token",
        }
    )

def test_refresh_access_token_http_error(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")

    mocker.patch("src.core.tokenmanager.requests.post", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError, match="401 Unauthorized"):
        refresh_access_token("client-id", "client-secret", "refresh-token")

def test_refresh_access_token_missing_token(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}

    mocker.patch("src.core.tokenmanager.requests.post", return_value=mock_response)

    with pytest.raises(KeyError, match="access_token"):
        refresh_access_token("client-id", "client-secret", "refresh-token")