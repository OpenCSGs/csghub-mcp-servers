import requests
import logging
import random
import json
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_list_inferences(token: str, username: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
        "deploy_type": 1  # As for inference deploy
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/run/model"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user inferences on {url}: {response.text}")
        return wrap_error_response(response)
    
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "deploy_id": res["deploy_id"],
            "deploy_name": res["deploy_name"],
            "model_id": res["model_id"],
            "runtime_framework": res["runtime_framework"],
            "status": res["status"],
        })

    return res_data

def api_get_inference_status(token: str, model_id: str, deploy_id: int) -> dict:
    """Get inference deployment status.
    
    Args:
        token: User access token
        model_id: Model repository path
        deploy_id: Deployment ID
        
    Returns:
        Inference status data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/run/{deploy_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get inferences status on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()

    json_data = response.json()
    res_data = {}
    
    if json_data and "data" in json_data:
        job_data = json_data["data"]
        status = job_data["status"]

        res_data = {
            "deploy_id": job_data["deploy_id"],
            "deploy_name": job_data["deploy_name"],
            "status": status,
        }

        if status.lower() == "running":
            web_access_url = f"{config.web_endpoint}/endpoints/{model_id}/{deploy_id}?tab=summary"
            api_access_endpoint = f"https://{job_data['endpoint']}/v1/chat/completions"
            curl_cmd = f"curl -X POST \"{api_access_endpoint}\" -H \"Content-Type: application/json\""
            payload = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is deep learning?"}
                ],
                "stream": True
            }
            test_command = f"{curl_cmd} -d '{json.dumps(payload)}'"
            res_data["web_access_url"] = web_access_url
            res_data["api_access_endpoint"] = api_access_endpoint
            res_data["test_command"] = test_command

    return res_data

def api_inference_create(
    token: str,
    model_id: str,
    cluster_id: str,
    runtime_framework_id: int,
    resource_id: int,
    entrypoint: str,
    agents: str = "",
):
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/run"
    random_num = f"{random.randint(0, 9999):04d}"
    json_data = {
        "cluster_id": cluster_id,
        "runtime_framework_id": runtime_framework_id,
        "resource_id": resource_id,
        "cost_per_hour": 0,
        "deploy_name": f"deploy_{random_num}",
        "env": "",
        "hardware": "",
        "max_replica": 1,
        "min_replica": 1,
        "revision": "main",
        "secure_level": 1,
        "entrypoint": entrypoint,
        "agents": agents,
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code != 200:
        logger.error(f"failed to create model inference on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        job_data = json_data["data"]
        res_data = {"deploy_id": job_data["deploy_id"]}

    return res_data

def api_inference_stop(token: str, model_id: str, deploy_id: int):
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/run/{deploy_id}/stop"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to stop model inference on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def api_inference_start(token: str, model_id: str, deploy_id: int):
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/run/{deploy_id}/start"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to start model inference on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def api_inference_delete(token: str, model_id: str, deploy_id: int):
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/run/{deploy_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete model inference on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()


