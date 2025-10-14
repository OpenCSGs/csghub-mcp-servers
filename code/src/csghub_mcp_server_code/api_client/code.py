import requests
import logging

logger = logging.getLogger(__name__)

def api_list_codes(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/codes"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user codes on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_get_code_details(api_url: str, token: str, code_path: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/codes/{code_path}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get code details on {url}: {response.text}")

    response.raise_for_status()
    return response.json()