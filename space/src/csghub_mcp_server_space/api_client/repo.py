import requests
import logging
from .constants import get_csghub_config

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
        api_url: CSGHub API base URL
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

    response.raise_for_status()
    return response.json()

def detail(
    token: str,
    repo_type: str,
    namespace: str,
    repo_name: str
) -> dict:
    """
    Get repo details.

    Args:
        api_url: CSGHub API base URL.
        token: User's token.
        repo_type: Type of the repo, e.g. "space", "model", "dataset", "code".
        namespace: Namespace of the user or organization.
        repo_name: Name of the repo.

    Returns:
        Response data.
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/{repo_type}s/{namespace}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get repo detail on {url}: {response.text}")

    response.raise_for_status()
    return response.json()