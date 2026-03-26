import logging
import os
import subprocess
import threading
import time
from typing import Any, Dict, Optional

from dotenv import load_dotenv

import google.auth
import google.auth.transport.requests
import google.cloud.logging
import google.oauth2.id_token
from google.auth.transport.requests import Request as GoogleAuthRequest

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams, StreamableHTTPConnectionParams
from google.adk.tools.tool_context import ToolContext

# --- Setup Logging and Environment ---

# cloud_logging_client = google.cloud.logging.Client()
# cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")

# Configure the MCP Tool to connect to the Propertiesz MCP server
mcp_server_url = os.getenv("MCP_SERVER_URL")
azure_mcp_server_url = os.getenv("AZURE_MCP_SERVER_URL")
azure_mcp_server_key = os.getenv("AZURE_MCP_SERVER_KEY")


# Token Cache state
_token_cache: Optional[str] = None
_token_expiry: float = 0
_token_lock = threading.Lock()

def _get_token_via_gcloud_cli() -> Optional[str]:
    """Attempts to fetch token via gcloud CLI (Local Dev fallback)."""
    try:
        print("--- Attempting to fetch token via gcloud CLI ---")
        access_token = subprocess.check_output(
            ["gcloud", "auth", "print-identity-token"], 
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        print("--- Access token fetched successfully via gcloud CLI ---")
        return access_token
    except Exception as e:
        print(f"--- gcloud CLI failed: {e} ---")
        return None

def _get_id_token():
    """Get an ID token to authenticate with the MCP server."""
    try:
        print("--- Attempting to fetch ID token ---")
        target_url = os.getenv("MCP_SERVER_URL")
        audience = target_url.split('/mcp/')[0]
        request = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(request, audience)
        print("--- ID token fetched successfully ---")
        return id_token
    except Exception as e:
        print(f"--- ID token fetch failed: {e} ---")
        return None


# Cloud Run expects an ID token
def get_id_token():
    global _token_cache, _token_expiry
    
    # 10 minutes buffer (ensures at least 50 mins reuse for 1hr token)
    buffer = 600
    now = time.time()
    
    with _token_lock:
        if _token_cache and now < (_token_expiry - buffer):
            print("--- Using Cached Access Token ---")
            return _token_cache
            
        # Try Method 1: google-auth
        token = _get_id_token()
        
        # Try Method 2: gcloud CLI fallback
        if not token:
            token = _get_token_via_gcloud_cli()
            
        if token:
            _token_cache = token
            _token_expiry = now + 3600 # Default lifetime
            return _token_cache
            
        return None


# Header provider to fetch gcloud access token on demand
def get_gcp_auth_header(context: ReadonlyContext) -> Dict[str, str]:
    token = get_id_token()
    return {"Authorization": f"Bearer {token}"} if token else {}

def get_azure_auth_header(tool_context: ToolContext) -> Dict[str, Any]:
    return {"x-functions-key": azure_mcp_server_key}

gcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=mcp_server_url),
    errlog=None,
    header_provider=get_gcp_auth_header
)

azure_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=azure_mcp_server_url),
    errlog=None,
    header_provider=get_azure_auth_header
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