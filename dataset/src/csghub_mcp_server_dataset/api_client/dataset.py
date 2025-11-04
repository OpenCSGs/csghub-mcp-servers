import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_list_datasets(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/datasets"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user datasets on {url}: {response.text}")

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "dataset_id": res["path"]
        })
    return res_data

def api_get_dataset_details(token: str, dataset_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/datasets/{dataset_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get dataset details on {url}: {response.text}")

    response.raise_for_status()
    json_data = response.json()
    res_data = {}

    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/datasets/{res['path']}"
        res_data = {
            "dataset_id": res["path"],
            "clone_address": res["repository"],
            "web_access_url": access_url,
        }

    return res_data

def api_create_dataset(
        token: str, 
        namespace: str,
        dataset_name: str,
        license: str,
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
        "name": dataset_name,
        "namespace": namespace,
        "private": True,
        "readme": readme,
    }
    url = f"{config.api_endpoint}/api/v1/datasets"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create dataset repo: {data} on {url} :{response.text}")

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/datasets/{res['path']}"
        res_data = {
            "dataset_id": res["path"],
            "web_access_url": access_url,
        }
    return res_data

def api_delete_dataset(token: str, dataset_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/datasets/{dataset_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete dataset on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_find_datasets_by_name(token: str, name: str, page: int = 1, page_size: int = 20) -> dict:
    config = get_csghub_config()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "page": page,
        "per": page_size,
        "search": name,
        "sort": "trending",
    }
    url = f"{config.api_endpoint}/api/v1/datasets"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get searched datasets on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    total = json_data["total"]
    for res in res_list:
        res_data.append({
            "dataset_id": res["path"],
        })

    return {"total_found": total, "datasets": res_data}
