import logging
import json
import base64
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    resources,
    user,
)
from .api_client import (
    space, repo, cluster,
    query_my_spaces,
    api_get_namespaces_by_token,
)

logger = logging.getLogger(__name__)

def register_space_tools(mcp_instance: FastMCP):
    register_space_create(mcp_instance)
    register_space_start(mcp_instance)
    register_space_stop(mcp_instance)
    register_space_delete(mcp_instance) 
    # register_file_upload(mcp_instance)
    register_space_detail(mcp_instance)
    register_list_my_space_tool(mcp_instance)

def register_space_create(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="create_space",
        title="Create and run a CSGHub space",
        description="""Creates a new CSGHub space, uploads files, and attempts to start it.
Parameters:
- `token` (str, required): User's API token.
- `name` (str, required): Name of the space.
- `cluster_id` (str, required): The cluster ID to deploy the space.
- `resource_id` (int, required): The resource ID for the space.
- `namespace` (str, optional): The user's namespace, default value is the username derived from the token.
- `sdk` (str, optional, default: 'gradio'): The SDK to use for the space.
- `license` (str, optional, default: 'apache-2.0'): The license for the space.
- `private` (bool, optional, default: False): Whether the space is private.
- `order_detail_id` (int, optional): Order detail ID.
- `env` (str, optional): Environment variables for the space.
- `secrets` (str, optional): Secrets for the space.
- `min_replica` (int, optional, default: 0): Minimum number of replicas for the space.
The final response includes results for creation, uploads, and the run attempt. 
In response, ["namespace"]["path"] can be used as namespace for other tool""",
        structured_output=True,
    )
    def create_space(
        token: str,
        name: str,
        resource_id: int,
        cluster_id: str,
        namespace: str = None,
        sdk: str = "gradio",
        license: str = "apache-2.0",
        private: bool = False,
        order_detail_id: int = 0,
        env: str = "",
        secrets: str = "",
        min_replica: int = 0,
    ) -> str:
        """
        Create a new CSGHub space, upload files, and run it.
        
        Args:
            token: User's API token.
            name: Name of the space.
            namespace: Namespace of the user.
            sdk: SDK for the space (default: gradio).
            license: License of the space (default: apache-2.0).
            private: Whether the space is private (default: False).
            order_detail_id: Order detail ID.
            env: Environment variables.
            secrets: Secrets for the space.
        """
        if namespace is None or len(namespace.strip()) < 1:
            try:
                namespace = api_get_username_from_token(token)
            except Exception as e:
                logger.error(f"Error calling user token API: {e}")
                return f"Error: Failed to get username. {e}"
        
        resp = {}

        create_resp = space.create(
            token=token,
            name=name,
            namespace=namespace,
            resource_id=resource_id,
            cluster_id=cluster_id,
            sdk=sdk,
            license=license,
            private=private,
            order_detail_id=order_detail_id,
            env=env,
            secrets=secrets,
            min_replica=min_replica,
        )
        resp['create_result'] = create_resp
        if "space_id" not in create_resp:
            return json.dumps(resp)
        
        namespace = create_resp["space_id"].split('/')[0]
        file = {
            'name': 'app.py',
            'content': '''import gradio as gr

def greet(name):
return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()'''
                }
   
        file_name = file.get('name')
        file_content = file.get('content')

        encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
        upload_resp = repo.upload_file(
            token=token,
            namespace=namespace,
            repo_name=name,
            file_path=file_name,
            content=encoded_content,
            repo_type="space",
            branch="main"
        ) 
        resp['upload_result'] = upload_resp

        return json.dumps(resp)


    @mcp_instance.tool(
        name="get_space_available_resource",
        title="Get available space resources",
        description="Get available space resources. Parameters: `token` (str, required): User's API token.",
        structured_output=True,
    )
    def get_space_available_resource(
        token: str,
    ) -> str:
        if not token:
            return "Error: The 'token' parameter is required."

        try:
            resp = resources.api_get_available_resources(
                token=token,
                deploy_type=0
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling get space resource API: {e}")
            return f"Error: Failed to get space resource. {e}"

    @mcp_instance.tool(
        name="get_user_namespaces",
        title="Get user's available namespaces",
        description="Get user's available namespaces for creating repositories. Parameters: `token` (str, required): User's token.",
        structured_output=True,
    )
    def get_user_namespaces_tool(token: str) -> str:
        """
        Get user's available namespaces.

        Args:
            token: User's token.
        """
        try:
            namespaces = api_get_namespaces_by_token(token)
            return json.dumps(namespaces)
        except Exception as e:
            logger.error(f"Error calling get user namespaces API: {e}")
            return f"Error: Failed to get user namespaces. {e}"

def register_file_upload(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="upload_space_file",
        title="Upload a file to a CSGHub space",
        description="Upload a file to a specified CSGHub space. Parameters: `token` (str, required): User's API token. `username` (str, required): The user's namespace. `space_name` (str, required): Name of the space. `file_name` (str, optional): Path of the file in the space repository (e.g., 'app.py'). `file_content` (str, optional): The raw content of the file to upload, defaults to a simple Gradio app. `branch` (str, optional, default: 'main'): The target branch.",
        structured_output=True,
    )
    def upload_file(
        token: str,
        username: str,
        space_name: str,
        file_name: str = "app.py",
        file_content: str = """import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs=\"text\", outputs=\"text\")
iface.launch()""",
        branch: str = "main"
    ) -> str:
        """
        Upload a file to a CSGHub space.

        Args:
            token: User's API token.
            username: The user's namespace.
            space_name: Name of the space.
            file_name: Path of the file in the space repository (e.g., 'app.py').
            file_content: The raw content of the file to upload. Defaults to a simple Gradio app.
            branch: The target branch (default: main).
        """

        if not token:
            return "Error: The 'token' parameter is required."
        if not username:
            return "Error: The 'username' parameter is required."
        if not space_name:
            return "Error: The 'space_name' parameter is required."

        try:
            encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
            resp = repo.upload_file(
                token=token,
                namespace=username,
                repo_name=space_name,
                file_path=file_name,
                content=encoded_content,
                repo_type="space",
                branch=branch
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling upload file API: {e}")
            return f"Error: Failed to upload file. {e}"

def register_space_start(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="start_space_by_id",
        title="Start a CSGHub space with access token.",
        description="Starts a CSGHub space. Parameters: `token` (str, required): User's API token. `space_id` (str, required): ID of the space to run. `space_id` is usually in the format of namespace/name. Example: 'user1/my-space'.",
        structured_output=True,
    )
    def start_space_by_id(
        token: str,
        space_id: str,
    ) -> str:
        """
        Run a CSGHub space.

        Args:
            token: User's API token.
            space_id: Name of the space.
        """

        if not token:
            return "Error: The 'token' parameter is required."

        try:
            resp = space.start(
                token=token,
                space_id=space_id,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling run space API: {e}")
            return f"Error: Failed to run space. {e}"

def register_space_stop(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="stop_space_by_id",
        title="Stop a CSGHub space by ID namespace/name with access token.",
        description="Stops a CSGHub space. Parameters: `token` (str, required): User's API token. `space_id` (str, required): Name of the space to stop. `space_id` is usually in the format of namespace/name. Example: 'user1/my-space'.",
        structured_output=True,
    )
    def stop_space_by_id(
        token: str,
        space_id: str,
    ) -> str:
        """
        Stop a CSGHub space.

        Args:
            token: User's API token.
            space_id: Name of the space.
        """

        if not token:
            return "Error: The 'token' parameter is required."

        try:
            resp = space.stop(
                token=token,
                space_id=space_id,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling stop space API: {e}")
            return f"Error: Failed to stop space. {e}"

def register_space_detail(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_space_detail_by_id",
        title="Get details or status of a CSGHub space",
        description="Retrieves details for a specific CSGHub space. Parameters: `token` (str, required): User's API token. `space_id` (str, required): ID of the space. `space_id` is usually in the format of namespace/name. Example: 'user1/my-space'.",
        structured_output=True,
    )
    def get_space_detail_by_id(
        token: str,
        space_id: str,
    ) -> str:
        """
        Get details of a CSGHub space.

        Args:
            token: User's API token.
            space_id: namespace/name of the space.
        """

        if not token:
            return "Error: The 'token' parameter is required."
        if not space_id:
            return "Error: The 'space_name' parameter is required."

        try:
            resp = repo.detail(
                token=token,
                space_id=space_id,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling get space detail API: {e}")
            return f"Error: Failed to get space detail. {e}"

def register_space_delete(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="delete_space_by_id",
        title="Delete a CSGHub space with access token",
        description="Deletes a CSGHub space. Parameters: `token` (str, required): User's API token. `space_id` (str, required): ID of the space to delete. `space_id` is usually in the format of namespace/name. Example: 'user1/my-space'.",
        structured_output=True,
    )
    def delete_space_by_id(
        token: str,
        space_id: str,
    ) -> str:
        """
        Delete a CSGHub space.

        Args:
            token: User's API token.
            space_id: Name of the space.
        """

        if not token:
            return "Error: The 'token' parameter is required."

        try:
            resp = space.delete(
                token=token,
                space_id=space_id,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling delete space API: {e}")
            return f"Error: Failed to delete space. {e}"

def register_list_my_space_tool(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_my_spaces",
        title="List spaces for a user from CSGHub",
        description="Retrieve a list of spaces for a specific user from CSGHub. Parameters: `token` (str, required): User's API token. `username` (str, required): The user's namespace. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_my_spaces(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."

        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"
        
        
        try:
            spaces = query_my_spaces(token, username, per, page)
            return json.dumps(spaces)
        except Exception as e:
            logger.error(f"Error calling list spaces API: {e}")
            return f"Error: Failed to list spaces. {e}"

