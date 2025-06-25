from src.core.views import addreviews
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


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

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Success")

        except Exception as e:
            print(f"Error occurred during process: {e.args[0]}")

            self.end_headers()
            self.send_response(500)
            self.wfile.write(b"Failure")


# if __name__ == "__main__":
#     # Set secret locally for testing
#     os.environ['CRON_SECRET'] = 'mysecrettoken'

#     server_address = ('', 8080)
#     httpd = HTTPServer(server_address, handler)
#     print("Serving on port 8080...")
#     httpd.serve_forever()