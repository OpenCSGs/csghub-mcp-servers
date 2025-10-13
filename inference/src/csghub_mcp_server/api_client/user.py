import requests
import logging

logger = logging.getLogger(__name__)

def api_get_username_from_token(api_url: str, api_key: str, token: str) -> str:
    """Get username from access token.
    
    Args:
        api_url: CSGHub API base URL
        api_key: API key for authentication
        token: User access token
        
    Returns:
        Username string
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{api_url}/api/v1/token/{token}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get username on {url}: {response.text}")

    response.raise_for_status()
    data = response.json()["data"]
    if "user_name" not in data:
        raise ValueError("'user_name' not in response from token API.")
    return data["user_name"]
