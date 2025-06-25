from src.core.views import addreviews
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print("Starting request")
        try:
            auth_header = self.headers.get('Authorization')
            expected_token = f"Bearer {os.environ.get('CRON_SECRET')}"

            if auth_header != expected_token:
                return {
                    "statusCode": 401,
                    "body": "Unauthorized"
                }

            print("Proper auth")
            addreviews.handler()

            print("Successfully added reviews to spreadsheet.")

            return {
                "statusCode": 200,
                "body": ""
            }

        except Exception as e:
            print(f"Error occurred during process: {e.args[0]}")
            return {
                "statusCode": 500,
                "body": str(e)
            }