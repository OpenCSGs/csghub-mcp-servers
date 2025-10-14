import logging
from mcp.server.fastmcp import FastMCP
import json
import base64
from .api_client import (
    api_get_username_from_token,
    api_get_top_download_spaces,
    create_space,
    run_space,
    get_space_resources,
    get_clusters
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_space_tools(mcp_instance: FastMCP):
    register_create_tools(mcp_instance)
    register_run_tool(mcp_instance)
    register_upload_tool(mcp_instance)
    register_query_resource_tool(mcp_instance)

def register_create_tools(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="create_space",
        title="Create a new CSGHub space",
        description="Create a new CSGHub space. Parameters: `token` (str, required): User's API token. `name` (str, required): Name of the space. `hardware` (int, required): Hardware required. `resource_id` (int, required): Resource ID for the hardware. `cluster_id` (str, required): ID of the cluster to deploy to. `sdk` (str, optional, default: 'gradio'): SDK for the space. `license` (str, optional, default: 'apache-2.0'): License of the space. `private` (bool, optional, default: False): Whether the space is private. `order_detail_id` (int, optional): Order detail ID. `env` (str, optional): Environment variables. `secrets` (str, optional): Secrets for the space.",
        structured_output=True,
    )
    def create_space(
        token: str,
        name: str,
        hardware: int,
        resource_id: int,
        cluster_id: str,
        sdk: str = "gradio",
        license: str = "apache-2.0",
        private: bool = False,
        order_detail_id: int = 0,
        env: str = "",
        secrets: str = ""
    ) -> str:
        """
        Create a new CSGHub space.
        
        Args:
            token: User's API token.
            name: Name of the space.
            namespace: Namespace of the user.
            hardware: Hardware required.
            resource_id: Resource ID for the hardware.
            cluster_id: ID of the cluster to deploy to.
            sdk: SDK for the space (default: gradio).
            license: License of the space (default: apache-2.0).
            private: Whether the space is private (default: False).
            order_detail_id: Order detail ID.
            env: Environment variables.
            secrets: Secrets for the space.
        """
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"
        
        try:
            resp = create_space(
                api_url=api_url,
                token=token,
                name=name,
                namespace=username,
                hardware=hardware,
                resource_id=resource_id,
                cluster_id=cluster_id,
                sdk=sdk,
                license=license,
                private=private,
                order_detail_id=order_detail_id,
                env=env,
                secrets=secrets
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling create space API: {e}")
            return f"Error: Failed to create space. {e}"

def register_upload_tool(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="upload_space_file",
        title="Upload a file to a CSGHub space",
        description="Upload a file to a specified CSGHub space. Parameters: `token` (str, required): User's API token. `space_name` (str, required): Name of the space. `file_name` (str, optional): Path of the file in the space repository (e.g., 'app.py'). `file_content` (str, optional): The raw content of the file to upload, defaults to a simple Gradio app. `branch` (str, optional, default: 'main'): The target branch.",
        structured_output=True,
    )
    def upload_file(
        token: str,
        space_name: str,
        file_name: str = "app.py",
        file_content: str = """import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()""",
        branch: str = "main"
    ) -> str:
        """
        Upload a file to a CSGHub space.

        Args:
            token: User's API token.
            space_name: Name of the space.
            remote_file_path: Path of the file in the space repository (e.g., 'app.py').
            file_content: The raw content of the file to upload. Defaults to a simple Gradio app.
            branch: The target branch (default: main).
        """
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()

        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        try:
            encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
            resp = upload_file(
                api_url=api_url,
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

def register_run_tool(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="run_space",
        title="Run a CSGHub space",
        description="Starts a CSGHub space. Parameters: `token` (str, required): User's API token. `space_name` (str, required): Name of the space to run.",
        structured_output=True,
    )
    def run_space(
        token: str,
        space_name: str,
    ) -> str:
        """
        Run a CSGHub space.

        Args:
            token: User's API token.
            space_name: Name of the space.
        """
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()

        if not token:
            return "Error: The 'token' parameter is required."
        if not space_name:
            return "Error: The 'space_name' parameter is required."

        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        try:
            resp = run_space(
                api_url=api_url,
                token=token,
                namespace=username,
                space_name=space_name,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling run space API: {e}")
            return f"Error: Failed to run space. {e}"

def register_query_resource_tool(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_space_resource",
        title="Get available space resources",
        description="Get available space resources. Parameters: `token` (str, required): User's API token. `cluster_id` (str, optional): ID of the cluster. If not provided, the first available cluster will be used.",
        structured_output=True,
    )
    def get_space_resource(
        token: str,
        cluster_id: str = ""
    ) -> str:
        """
        Get available space resources.

        Args:
            token: User's API token.
            cluster_id: ID of the cluster.
        """
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()

        if not token:
            return "Error: The 'token' parameter is required."

        try:
            # Verifying token is valid
            api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        try:
            final_cluster_id = cluster_id
            if not final_cluster_id:
                clusters_resp = get_clusters(api_url=api_url, token=token)
                clusters = clusters_resp.get('data', [])
                if clusters and len(clusters) > 0:
                    final_cluster_id = clusters[0].get('id')
                else:
                    return "Error: No available clusters found."

            resp = get_space_resources(
                api_url=api_url,
                token=token,
                cluster_id=final_cluster_id,
                deploy_type=0
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling get space resource API: {e}")
            return f"Error: Failed to get space resource. {e}"
