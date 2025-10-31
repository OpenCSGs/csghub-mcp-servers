import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_username_from_token(token: str) -> str:
    """Get username from access token.
    
    Args:
        api_url: CSGHub API base URL
        api_key: API key for authentication
        token: User access token
        
    Returns:
        Username string
    """
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


def get_user_namespaces(api_url: str, username: str) -> list[str]:
    """Get user's available namespaces for creating repositories.

    This includes the user's own username and the organizations they are a part of.

    Args:
        api_url: CSGHub API base URL
        username: Username

    Returns:
        A list of namespace strings.
    """
    url = f"{api_url}/api/v1/user/{username}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["data"]
    namespaces = [data["username"]]
    for org in data.get("orgs", []):
        namespaces.append(org["path"])
    return namespaces