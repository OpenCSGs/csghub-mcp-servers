import requests
import logging

logger = logging.getLogger(__name__)

def upload_file(
    api_url: str,
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
    url = f"{api_url}/api/v1/{repo_type}s/{namespace}/{repo_name}/raw/{file_path}"
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