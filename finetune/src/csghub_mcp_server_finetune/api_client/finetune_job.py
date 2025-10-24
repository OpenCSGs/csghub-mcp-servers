import requests
import logging
import random

logger = logging.getLogger(__name__)

def api_list_finetune_jobs(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/finetune/jobs"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user finetune jobs on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_get_finetune_job(api_url: str, token: str, job_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/finetunes/{job_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get finetune job on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_delete_finetune_job(api_url: str, token: str, job_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/finetunes/{job_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete finetune job on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_create_finetune_job(api_url: str, token: str, 
                            model_id: str, dataset_id: str, 
                            rf_id: int, res_id: int, 
                            epochs: int = 1, learning_rate: float = 0.0001) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{api_url}/api/v1/finetunes"
    random_num = f"{random.randint(0, 9999):04d}"
    data = {
        "task_name": f"finetune_job_{random_num}",
        "task_desc": "",
        "runtime_framework_id": rf_id,
        "resource_id": res_id,
        "model_id": model_id,
        "dataset_id": dataset_id,
        "epochs": epochs,
        "learning_rate": learning_rate,
        "share_mode": False,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create finetune job on {url}: {response.text}")

    response.raise_for_status()
    return response.json()
