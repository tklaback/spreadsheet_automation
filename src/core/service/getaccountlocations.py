from core.service.networkservice import Network

def get_locations(auth_token: str, account_number: str) -> list[str]:
    url = f"https://mybusinessbusinessinformation.googleapis.com/v1/accounts/{account_number}/locations?readMask=name"
    response = Network.build_request({
        "url": url,
        "method": "GET",
        "headers": {
            f"Bearer {auth_token}"
        }
    })

    locations = response.json().get("locations", [])

    return [locObj["name"].split('/')[1] for locObj in locations]

def get_account(auth_token: str) -> str:
    url = "https://mybusinessbusinessinformation.googleapis.com/v1/accounts"

    response = Network.build_request({
        "url": url,
        "method": "GET",
        "headers": {
            f"Bearer {auth_token}"
        }
    })

    accounts = response.json().get("accounts", [])

    for account_obj in accounts:
        account_num = account_obj["name"].split("/")[1]
        if get_locations(auth_token, account_num):
            return account_num
    
    raise Exception("No account number works")
