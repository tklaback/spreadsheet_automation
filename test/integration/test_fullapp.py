import pytest
import moto

@pytest.fixture
def test_full_app(monkeypatch, mocker):
    monkeypatch.setenv("CREDENTIALS_PATH", "creds")
    monkeypatch.setenv("SHEET_ID", "sheet_id")
    monkeypatch.setenv("SHEET_NAME", "sheet_name")
    monkeypatch.setenv("API_KEY", "api_key")
    monkeypatch.setenv("GOOGLE_SECRET_NAME", "secret_name")
    monkeypatch.setenv("SECRET_ID", "secret_id")

     