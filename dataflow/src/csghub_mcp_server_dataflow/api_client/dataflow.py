import requests
import logging
import random
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_list_jobs(token: str, per: int = 10, page: int = 1) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "query": "",
        "page_size": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/dataflow/jobs"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list dataflow jobs on {url}: {response.text}")
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
            "job_id": res["job_id"],
            "job_name": res["job_name"],
            "job_type": res["job_type"],
            "status": res["status"],
        })
    return res_data

def api_get_job_details(token: str, job_id: int, job_type: str = "data_refine") -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/dataflow/jobs/{job_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get dataflow job details on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()
    res_data = {}

    if json_data and "job" in json_data:
        res = json_data["job"]
        access_url = f"{config.web_endpoint}/datapipelines/dataflowInfo?id={job_id}&type=pipeline&jobType={job_type}"
        res_data = {
            "job_id": res["job_id"],
            "job_name": res["job_name"],
            "status": res["status"],
            "finished_at": res["date_finish"],
            "output_branch_name": res["export_branch_name"],
            "web_access_url": access_url,
        }

    return res_data

def api_get_template_list(token: str, page: int, page_size: int) -> dict:
    templates = []
    res_list = read_templates(token, page, page_size)
    for res in res_list:
        templates.append({
            "template_id": res["id"],
            "template_name": res["name"],
            "template_type": res["type"],
            # "template_dsl_text": res["dslText"],
        })

    return templates

def read_templates(token: str, page: int, page_size: int) -> list:
    config = get_csghub_config()
    params = {
        "page_size": page_size,
        "page": page,
    }
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/dataflow/algo_templates"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get dataflow templates on {url} :{response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    json_data = response.json()

    templates = []
    res_data = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_data, object):
        return templates
    
    res_list = res_data["templates"] if res_data and "templates" in res_data else []
    if not isinstance(res_list, list):
        return templates
    
    return res_list

def get_template_by_id(token: str, template_id: int) -> dict | None:
    config = get_csghub_config()

    headers = {"Authorization": f"Bearer {token}"}

    url = f"{config.api_endpoint}/api/v1/dataflow/algo_templates/{template_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get dataflow template on {url} :{response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    template = None
    json_data = response.json()
    res_data = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_data, object):
        return template
    
    template =  {
        "template_id": res_data["id"],
        "template_name": res_data["name"],
        "template_type": res_data["type"],
        "template_dsl_text": res_data["dslText"],
    }
    return template

def api_create_job(
        token: str, 
        template_id: int,
        username: str, 
        dataset_id: str,
        branch: str,
        text_keys: str,
) -> dict:
    config = get_csghub_config()
    template = get_template_by_id(token, template_id)
    if not template:
        raise Exception("Template not found")
    
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    random_num = f"{random.randint(0, 9999):04d}"
    project_name = f"job-{random_num}"
    data = {
        "name": template["template_name"],
        "type": template["template_type"],
        "description": "",
        "owner": username,
        "project_name": project_name,
        "repo_id": dataset_id,
        "branch": branch,
        "text_keys": text_keys,
        "dataset_path": "",
        "export_path": "",
        "is_run": True,
        "process":[],
        "dslText": template["template_dsl_text"],
    }
    url = f"{config.api_endpoint}/api/v1/dataflow/jobs/pipeline"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"failed to create dataflow job on {url} :{response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/datapipelines/dataflowInfo?id={res['job_id']}&type=pipeline"
        res_data = {
            "job_id": res["job_id"],
            "job_name": res["job_name"],
            "status": res["status"],
            "web_access_url": access_url,
        }
    return res_data

def api_delete_job(token: str, job_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/dataflow/jobs/{job_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete dataflow job on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    return response.json()
