import time
import requests

class Network:
    @staticmethod
    def _request_with_retries(config, max_retries=3):
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.request(
                    method=config.get("method"),
                    url=config.get("url"),
                    headers=config.get("headers"),
                    params=config.get("params"),
                    data=config.get("data"),
                    timeout=config.get("timeout", 10)
                )

                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as err:
                status = getattr(err.response, 'status_code', None)
                attempt += 1

                if status and 400 <= status < 500 and status != 429:
                    raise err

                backoff_ms = 200 * (2 ** attempt)
                time.sleep(backoff_ms / 1000)

        raise Exception(f"Request failed after {max_retries} retries")

    @staticmethod
    def build_request(config, max_retries=3):
        if not config.get("url") or not config.get("method"):
            raise ValueError("Config must contain 'url' and 'method'")

        return Network._request_with_retries(config, max_retries)
