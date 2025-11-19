import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_list_codes(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/codes"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user codes on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "code_id": res["path"]
        })
    return res_data

def api_get_code_details(token: str, code_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/codes/{code_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get code details on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()
    res_data = {}

    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/codes/{res['path']}"
        res_data = {
            "code_id": res["path"],
            "clone_address": res["repository"],
            "web_access_url": access_url,
        }

    return res_data

def api_create_code(
        token: str, 
        namespace: str,
        code_name: str,
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
        "name": code_name,
        "namespace": namespace,
        "private": True,
        "readme": readme,
    }
    url = f"{config.api_endpoint}/api/v1/codes"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create code repo: {data} on {url} :{response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/codes/{res['path']}"
        res_data = {
            "code_id": res["path"],
            "web_access_url": access_url,
        }
    return res_data

def api_delete_code(token: str, code_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/codes/{code_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete code on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    return response.json()
