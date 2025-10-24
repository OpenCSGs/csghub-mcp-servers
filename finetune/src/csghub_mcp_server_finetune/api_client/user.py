import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_username_from_token(token: str) -> str:
    config = get_csghub_config()
    
    headers = {"Authorization": f"Bearer {config.api_key}"}
    url = f"{config.api_endpoint}/api/v1/token/{token}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get username on {url}: {response.text}")

    response.raise_for_status()
    data = response.json()["data"]
    if "user_name" not in data:
        raise ValueError("'user_name' not in response from token API.")
    return data["user_name"]
