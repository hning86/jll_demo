import os
import logging
import google.cloud.logging
from dotenv import load_dotenv
from typing import Dict, Any

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams, SseConnectionParams
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.code_executors import VertexAiCodeExecutor

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token
from google.auth.transport.requests import Request as GoogleAuthRequest

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")

# Configure the MCP Tool to connect to the Propertiesz MCP server
mcp_server_url = os.getenv("MCP_SERVER_URL")
azure_mcp_server_url = os.getenv("AZURE_MCP_SERVER_URL")
azure_mcp_server_key = os.getenv("AZURE_MCP_SERVER_KEY")

def get_id_token():
    """Get an ID token to authenticate with the MCP server."""
    print("getting id token...")
    target_url = os.getenv("MCP_SERVER_URL")
    audience = target_url.split('/mcp/')[0]
    request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(request, audience)
    # print("got id token: ", id_token)
    return id_token

def get_auth_header(tool_context: ToolContext) -> Dict[str, Any]:
    token = get_id_token()
    return {"Authorization": f"Bearer {token}"}

def get_azure_auth_header(tool_context: ToolContext) -> Dict[str, Any]:
    return {"x-functions-key": azure_mcp_server_key}

gcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=mcp_server_url),
    errlog=None,
    header_provider=get_auth_header
)

azure_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=azure_mcp_server_url),
    errlog=None,
    header_provider=get_azure_auth_header
)

root_agent_test = Agent(
    name="property_agent",
    model=model_name,
    description="The primary researcher that can access both property data and external knowledge.",
    instruction="""
    You are a helpful commercial real estate property agent. Your goal is to fully answer user's questions by using the gcp_tools to get specific data about properties under the management (address, property type, price etc.). And then add some colorful descriptions based what you can infer from the properties data.
    """,
    tools=[gcp_tools]
)

root_agent = Agent(
    name="property_agent",
    model=model_name,
    description="The primary researcher that can access both property data and external knowledge.",
    instruction="""
    You are a helpful commercial real estate property agent. First greet user using the azure_tools. Then your goal is to fully answer user's questions by using the gcp_tools to get specific data about properties under the management (address, property type, price etc.). And then add some colorful descriptions based what you can infer from the properties data. You can also let users save their favorite property ID with azure_tools and retrieve it later. 
    """,
    tools=[gcp_tools, azure_tools]
)