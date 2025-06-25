from src.core.views.addreviews import handler
import os

def app(request):
    auth_header = request.headers.get('Authorization')
    expected_token = f"Bearer {os.environ.get('CRON_SECRET')}"

    if auth_header != expected_token:
        return {
            "statusCode": 401,
            "body": "Unauthorized"
        }

    return handler()
