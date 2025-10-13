import requests
import logging

logger = logging.getLogger(__name__)

def api_list_evaluations(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    """List evaluation services for a user.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Evaluation services data
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/evaluations"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user evaluations on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_get_evaluation_details(api_url: str, token: str, id: int) -> dict:
    """Get evaluaton details.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        id: Evaluation ID
        
    Returns:
        evaluation data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/evaluations/{id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get evaluation details on {url}: {response.text}")

    response.raise_for_status()
    return response.json()