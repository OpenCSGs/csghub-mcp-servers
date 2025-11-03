import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_top_download_models(num: int) -> dict:
    """Get top downloaded models.
    
    Args:
        num: Number of models to retrieve
        
    Returns:
        Top models data
    """
    config = get_csghub_config()

    headers = {"Content-Type": "application/json"}
    params = {
        "page": 1,
        "per": num,
        "search": "",
        "sort": "most_download"
    }
    url = f"{config.api_endpoint}/api/v1/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get top {num} downloaded models on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        access_url = f"{config.web_endpoint}/models/{res['path']}"
        git_clone_cmd = f"git clone {res['repository']['http_clone_url']}"
        res_data.append({
            "model_id": res["path"],
            "downloads": res["downloads"],
            "git_clone_command": git_clone_cmd,
            "access_url": access_url,
        })

    return res_data

def api_list_user_models(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user models on {url}: {response.text}")

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "model_id": res["path"]
        })

    return res_data

def api_get_model_details(token: str, model_id: str) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model details on {url}: {response.text}")

    response.raise_for_status()
    json_data = response.json()
    res_data = {}

    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/models/{res['path']}"
        res_data = {
            "model_id": res["path"],
            "clone_address": res["repository"],
            "web_access_url": access_url,
        }

    return res_data

def api_create_model(
        token: str, 
        namespace: str,
        model_name: str,
        license: str = "apache-2.0",
        readme: str = "", 
        description: str = "",
) -> dict:
    config = get_csghub_config()

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
    url = f"{config.api_endpoint}/api/v1/models"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create model repo: {data} on {url} :{response.text}")

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/models/{res['path']}"
        res_data = {
            "model_id": res["path"],
            "web_access_url": access_url,
        }
    return res_data

def api_delete_model(token: str, model_id: str) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete model on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_find_models_by_name(token: str, name: str, page: int = 1, page_size: int = 20) -> dict:
    config = get_csghub_config()

    headers = {"Content-Type": "application/json"}
    params = {
        "page": page,
        "per": page_size,
        "search": name,
        "sort": "trending",
    }
    url = f"{config.api_endpoint}/api/v1/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get searched models on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "model_id": res["path"],
        })

    return res_data
