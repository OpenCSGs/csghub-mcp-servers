import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)
  
def start(
    token: str,
    space_id: str
) -> dict:
    """
    Run a space.

    Args:
        token: User's token.
        space_id: Name of the space.

    Returns:
        Response data.
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/spaces/{space_id}/run"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to run space on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def create(
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
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/spaces"
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
        return wrap_error_response(response)
        
    response.raise_for_status()
    json_data = response.json()
    
    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        res_data = {
            "space_id": res["path"],
            "private": res["private"],
            "sdk_type": res["sdk"],
        }

    return res_data

def stop(
    token: str,
    space_id: str
) -> dict:
    """
    Stop a space.

    Args:
        token: User's token.
        space_id: Name of the space.

    Returns:
        Response data.
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/spaces/{space_id}/stop"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to stop space on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def delete(
    token: str,
    space_id: str
) -> dict:
    """Delete a space.
    
    Args:
        token: User's token
        space_id: Name of the space
        
    Returns:
        Response data
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/spaces/{space_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete space on {url}: {response.text}")
        return wrap_error_response(response)
        
    response.raise_for_status()
    return response.json()

def query_my_spaces(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    """List spaces of a user.
    
    Args:
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Space services data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/spaces"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user spaces on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data
    
    for res in res_list:
        res_data.append({
            "space_id": res["path"],
            "status": res["status"],
            "private": res["private"],
            "sdk_type": res["sdk"],
        })

    return res_data
