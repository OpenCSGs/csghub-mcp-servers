import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def upload_file(
    token: str,
    namespace: str,
    repo_name: str,
    file_path: str,
    content: str,
    repo_type: str,
    branch: str = "main"
) -> dict:
    """Upload a file to a repository.

    Args:
        token: User's token
        namespace: Namespace of the user
        repo_name: Name of the repository
        file_path: Path of the file in the repository
        content: Base64 encoded content of the file
        repo_type: Type of the repository (e.g., 'space', 'model')
        branch: Branch to commit to

    Returns:
        Response data
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/{repo_type}s/{namespace}/{repo_name}/raw/{file_path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": content,
        "message": f"Create {file_path}",
        "branch": branch,
        "new_branch": branch
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201 and response.status_code != 200:
        logger.error(f"failed to upload file to {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    return response.json()

def detail(
    token: str,
    space_id: str
) -> dict:
    """
    Get repo details.

    Args:
        token: User's token.
        space_id: Name of the repo.

    Returns:
        Response data.
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/spaces/{space_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get space id {space_id} detail: on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = {}
    if json_data and "data" in json_data:
        res = json_data["data"]
        access_url = f"{config.web_endpoint}/spaces/{res['path']}"
        res_data = {
            "space_id": res["path"],
            "status": res["status"],
            "sdk_type": res["sdk"],
            "web_access_url": access_url,
        }

    return res_data