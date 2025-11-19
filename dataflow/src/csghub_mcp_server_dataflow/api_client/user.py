import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_username_from_token(token: str) -> str:
    """Get username from access token.
    
    Args:
        token: User access token
        
    Returns:
        Username string
    """
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/token/{token}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get username on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    data = response.json()["data"]
    if "user_name" not in data:
        return {
            "error_message": "no user_name response from API.",
        }
    return data["user_name"]
