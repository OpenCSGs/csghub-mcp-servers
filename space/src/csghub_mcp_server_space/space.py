import logging
from mcp.server.fastmcp import FastMCP
import json
import base64
from .api_client import (
    api_get_username_from_token,
    api_get_top_download_spaces,
)
from .api_client import space, repo, space_resources, cluster
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_space_tools(mcp_instance: FastMCP):
    register_create_tools(mcp_instance)
    # register_run_tool(mcp_instance)
    # register_upload_tool(mcp_instance)
    register_query_resource_tool(mcp_instance)

def register_create_tools(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="create_space",
        title="Create and run a CSGHub space",
        description="""Creates a new CSGHub space, uploads files, and attempts to start it.
Parameters:
- `token` (str, required): User's API token.
- `name` (str, required): Name of the space.
- `files` (list, optional): A list of file dictionaries to upload, each with 'name' and 'content'. If omitted, a default 'app.py' is created.
- `cluster_id` (str, optional): Cluster ID for deployment. If omitted, the first available cluster is used.
- `resource_id` (int, optional): Hardware resource ID. If omitted, the first available resource in the cluster is used.
- `sdk` (str, optional, default: 'gradio'): The SDK to use.
- `license` (str, optional, default: 'apache-2.0'): The space license.
- `private` (bool, optional, default: False): Whether the space is private.
The final response includes results for creation, uploads, and the run attempt.""",
        structured_output=True,
    )
    def create_space(
        token: str,
        name: str,
        files: list | None = None,
        resource_id: int = 0,
        cluster_id: str = "",
        sdk: str = "gradio",
        license: str = "apache-2.0",
        private: bool = False,
        order_detail_id: int = 0,
        env: str = "",
        secrets: str = ""
    ) -> str:
        """
        Create a new CSGHub space, upload files, and run it.
        
        Args:
            token: User's API token.
            name: Name of the space.
            files: A list of file dictionaries to upload.
            namespace: Namespace of the user.
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
        
        final_cluster_id = cluster_id
        if not final_cluster_id:
            try:
                clusters_resp = cluster.get_clusters(api_url=api_url, token=token)
                clusters = clusters_resp.get('data', [])
                if clusters and len(clusters) > 0:
                    final_cluster_id = clusters[0].get('cluster_id')
                else:
                    return "Error: No available clusters found."
            except Exception as e:
                logger.error(f"Failed to get cluster list: {e}")
                return f"Error: Could not fetch the list of available clusters. {e}"

        final_resource_id = resource_id
        if not final_resource_id:
            try:
                resources_resp = space_resources.get_space_resources(
                    api_url=api_url,
                    token=token,
                    cluster_id=final_cluster_id,
                    deploy_type=0
                )
                resources = resources_resp.get('data', [])
                if resources and len(resources) > 0:
                    final_resource_id = resources[0].get('id')
                else:
                    return f"Error: No available resources found for cluster {final_cluster_id}."
            except Exception as e:
                logger.error(f"Failed to get resource list for cluster {final_cluster_id}: {e}")
                return f"Error: Could not fetch resources for cluster {final_cluster_id}. {e}"

        try:
            resp = space.create_space(
                api_url=api_url,
                token=token,
                name=name,
                namespace=username,
                resource_id=final_resource_id,
                cluster_id=final_cluster_id,
                sdk=sdk,
                license=license,
                private=private,
                order_detail_id=order_detail_id,
                env=env,
                secrets=secrets
            )

            if 'data' in resp:
                files_to_upload = files
                if not files_to_upload:
                    files_to_upload = [{
                        'name': 'app.py',
                        'content': '''import gradio as gr

def greet(name):
    return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()'''
                        }]
                    
                upload_results = []
                for file_info in files_to_upload:
                    file_name = file_info.get('name')
                    file_content = file_info.get('content')
                    if not file_name or not file_content:
                        upload_results.append({'error': f"Skipped invalid file entry: {file_info}"})
                        continue

                    try:
                        encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
                        upload_resp = repo.upload_file(
                            api_url=api_url,
                            token=token,
                            namespace=username,
                            repo_name=name,
                            file_path=file_name,
                            content=encoded_content,
                            repo_type="space",
                            branch="main"
                        )
                        upload_results.append(upload_resp)
                    except Exception as upload_e:
                        upload_results.append({'error': f"Failed to upload {file_name}: {str(upload_e)}"})
                    
                resp['upload_results'] = upload_results

                try:
                    run_resp = space.run_space(
                        api_url=api_url,
                        token=token,
                        namespace=username,
                        space_name=name,
                    )
                    resp['run_result'] = run_resp
                except Exception as run_e:
                    logger.error(f"Failed to run space {name}: {run_e}")
                    resp['run_result'] = {'error': f"Failed to run space: {str(run_e)}"}

            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error during core transaction (create, upload, or run): {e}")
            return f"Error: Failed during the core operation (create, upload, or run). {e}"


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
            resp = repo.upload_file(
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
            resp = space.run_space(
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
                clusters_resp = cluster.get_clusters(api_url=api_url, token=token)
                clusters = clusters_resp.get('data', [])
                if clusters and len(clusters) > 0:
                    final_cluster_id = clusters[0].get('id')
                else:
                    return "Error: No available clusters found."

            resp = space_resources.get_space_resources(
                api_url=api_url,
                token=token,
                cluster_id=final_cluster_id,
                deploy_type=0
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling get space resource API: {e}")
            return f"Error: Failed to get space resource. {e}"
