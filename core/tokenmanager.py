import os
import json
import boto3
import requests

# Secrets Manager helper
def get_google_secrets():
    """
    Expects an AWS Secrets Manager secret whose SecretString is JSON with keys:
      {
        "client_id": "...",
        "client_secret": "...",
        "refresh_token": "...",
        "account_id": "your-accounts/123456",
        "location_id": "locations/7890"
      }
    """
    secret_name = os.environ["GOOGLE_SECRET_NAME"]
    region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region)
    resp = client.get_secret_value(SecretId=secret_name)
    return json.loads(resp["SecretString"])

def refresh_access_token(client_id, client_secret, refresh_token):
    """
    Exchanges a refresh_token for a new access_token.
    """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id":     client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type":    "refresh_token",
    }
    r = requests.post(token_url, data=payload)
    r.raise_for_status()
    return r.json()["access_token"]

def fetch_business_reviews(access_token, account_id, location_id):
    """
    Calls the Google Business Profile API to list reviews.
    """
    url = f"https://businessprofile.googleapis.com/v1/{account_id}/{location_id}/reviews"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def lambda_handler(event, context):
    # 1. Load credentials & IDs from Secrets Manager
    secrets = get_google_secrets()
    client_id     = secrets["client_id"]
    client_secret = secrets["client_secret"]
    refresh_token = secrets["refresh_token"]
    account_id    = secrets["account_id"]
    location_id   = secrets["location_id"]

    # 2. Refresh the access token
    access_token = refresh_access_token(client_id, client_secret, refresh_token)

    # 3. Fetch reviews
    reviews = fetch_business_reviews(access_token, account_id, location_id)

    # 4. Return or process as you like
    return {
        "statusCode": 200,
        "body": json.dumps(reviews)
    }
