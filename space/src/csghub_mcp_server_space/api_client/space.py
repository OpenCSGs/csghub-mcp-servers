import requests
import logging

logger = logging.getLogger(__name__)

def api_get_top_download_spaces(api_url: str, num: int) -> dict:
    """Get top downloaded spaces.
    
    Args:
        api_url: CSGHub API base URL
        num: Number of spaces to retrieve
        
    Returns:
        Top spaces data
    """
    headers = {"Content-Type": "application/json"}
    params = {
        "page": 1,
        "per": num,
        "search": "",
        "sort": "most_download"
    }
    url = f"{api_url}/api/v1/spaces"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get spaces on {url}: {response.text}")
        
    response.raise_for_status()
    return response.json()

    
def start(
    api_url: str,
    token: str,
    namespace: str,
    space_name: str
) -> dict:
    """
    Run a space.

    Args:
        api_url: CSGHub API base URL.
        token: User's token.
        namespace: Namespace of the user.
        space_name: Name of the space.

    Returns:
        Response data.
    """
    url = f"{api_url}/api/v1/spaces/{namespace}/{space_name}/run"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to run space on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def create(
    api_url: str,
    token: str,
    name: str,
    namespace: str,
    resource_id: int,
    cluster_id: str,
    sdk: str = "gradio",
    license: str = "apache-2.0",
    private: bool = False,
    order_detail_id: int = 0,
    env: str = "",
    secrets: str = ""
) -> dict:
    """Create a new space.
    
    Args:
        api_url: CSGHub API base URL
        token: User's token
        name: Name of the space
        namespace: Namespace of the user
        resource_id: Resource ID
        cluster_id: Cluster ID
        sdk: SDK for the space
        license: License of the space
        private: Whether the space is private
        order_detail_id: Order detail ID
        env: Environment variables
        secrets: Secrets
        
    Returns:
        New space data
    """
    url = f"{api_url}/api/v1/spaces"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "namespace": namespace,
        "license": license,
        "sdk": sdk,
        "resource_id": resource_id,
        "cluster_id": cluster_id,
        "private": private,
        "order_detail_id": order_detail_id,
        "env": env,
        "secrets": secrets
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        logger.error(f"failed to create space on {url}: {response.text}")
        
    response.raise_for_status()
    return response.json()

def stop(
    api_url: str,
    token: str,
    namespace: str,
    space_name: str
) -> dict:
    """
    Stop a space.

    Args:
        api_url: CSGHub API base URL.
        token: User's token.
        namespace: Namespace of the user.
        space_name: Name of the space.

    Returns:
        Response data.
    """
    url = f"{api_url}/api/v1/spaces/{namespace}/{space_name}/stop"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to stop space on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def delete(
    api_url: str,
    token: str,
    namespace: str,
    repo_name: str
) -> dict:
    """Delete a space.
    
    Args:
        api_url: CSGHub API base URL
        token: User's token
        namespace: Namespace of the user
        repo_name: Name of the space
        
    Returns:
        Response data
    """
    url = f"{api_url}/api/v1/spaces/{namespace}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete space on {url}: {response.text}")
        
    response.raise_for_status()
    return response.json()
