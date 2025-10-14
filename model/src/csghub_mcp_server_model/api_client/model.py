import requests
import logging

logger = logging.getLogger(__name__)

def api_top_download_models(api_url: str, num: int) -> dict:
    """Get top downloaded models.
    
    Args:
        api_url: CSGHub API base URL
        num: Number of models to retrieve
        
    Returns:
        Top models data
    """
    headers = {"Content-Type": "application/json"}
    params = {
        "page": 1,
        "per": num,
        "search": "",
        "sort": "most_download"
    }
    url = f"{api_url}/api/v1/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get top {num} downloaded models on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()

def api_list_user_models(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user models on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_get_model_details(api_url: str, token: str, model_path: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_path}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model details on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_create_model(
        api_url: str, 
        token: str, 
        namespace: str,
        model_name: str,
        license: str = "apache-2.0",
        readme: str = "", 
        description: str = "",
) -> dict:
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    data = {
        "default_branch": "main",
        "description": description,
        "license": license,
        "name": model_name,
        "namespace": namespace,
        "private": True,
        "readme": readme,
    }
    url = f"{api_url}/api/v1/models"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create model repo: {data} on {url} :{response.text}")

    response.raise_for_status()
    return response.json()
