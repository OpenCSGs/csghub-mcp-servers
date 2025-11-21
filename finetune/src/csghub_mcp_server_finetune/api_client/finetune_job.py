import requests
import logging
import random
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_list_finetune_jobs(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/finetune/jobs"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user finetune jobs on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        finetuned_model_name = res["result_url"]
        job = {
            "id": res["id"],
            "task_name": res["task_name"],
            "status": res["status"],
            "finetuned_model_name": finetuned_model_name,
        }
        if res["status"].lower() == "succeeded":
            job["finetuned_model_address"] = f"{config.web_endpoint}/models/{finetuned_model_name}"

        res_data.append(job)

    return res_data

def api_get_finetune_job(token: str, job_id: int) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/finetunes/{job_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get finetune job on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()
    res_data = {}
    
    if json_data and "data" in json_data:
        job_data = json_data["data"]
        finetuned_model_name = job_data["result_url"]
        res_data = {
            "id": job_data["id"],
            "task_name": job_data["task_name"],
            "status": job_data["status"],
            "finetuned_model_name": finetuned_model_name,
        }
        if job_data["status"].lower() == "succeeded":
            res_data["finetuned_model_address"] = f"{config.web_endpoint}/models/{finetuned_model_name}"

    return res_data

def api_delete_finetune_job(token: str, job_id: int) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/finetunes/{job_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete finetune job on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def api_create_finetune_job(token: str, 
                            model_id: str, dataset_id: str, 
                            rf_id: int, res_id: int, 
                            epochs: int = 1, learning_rate: float = 0.0001,
                            agent: str = "") -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/finetunes"
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
        "agent": agent,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create finetune job on {url}: {response.text}")
        return wrap_error_response(response)

    json_data = response.json()
    res_data = {}
    if json_data and "data" in json_data:
        job_data = json_data["data"]
        res_data = {
            # "id": job_data["id"],
            "task_name": job_data["task_name"],
            "status": job_data["status"],
        }

    return res_data

def api_query_finetune_job_logs(token: str, job_id: int, since: str) -> dict:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/finetunes/{job_id}/logs"
    params = {
        "since": since,
        "stream": "false",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get finetune job jobs on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()
    res_data = {"logs": json_data["data"]}
    return res_data

if __name__ == "__main__":
    token = ""
    model_id = "wanghh2003/Qwen3-0.6B"
    dataset_id = "wanghh2003/finetune-data"
    # result = api_list_finetune_jobs(token, "wanghh2003")
    # result = api_get_finetune_job(oken, 365)
    result = api_create_finetune_job(token, model_id, dataset_id, rf_id=183, res_id=4)
    print(result)
