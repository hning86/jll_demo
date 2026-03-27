import os
from typing import Dict, Any

import google.auth.transport.requests
import google.oauth2.id_token
from google.adk.tools.tool_context import ToolContext

class TokenManager:
    """Manages Google ID tokens, including caching and fallbacks."""

    def __init__(self):
        self._cached_token: str | None = None
        self._cached_token_expiry: float = 0.0

    def _get_id_token_via_gcloud(self, audience: str) -> str | None:
        """Fallback method to get ID token via gcloud command line."""
        try:
            import subprocess
            result = subprocess.run(
                ["gcloud", "auth", "print-identity-token"],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            if token:
                print("Successfully retrieved token using gcloud.")
                return token
        except Exception as e:
            print(f"Fallback gcloud retrieval failed: {e}")
        return None

    def _get_token_expiry(self, token: str) -> float:
        """Decodes JWT payload to extract the 'exp' claim.

        Args:
            token: The ID token string.

        Returns:
            The 'exp' claim as a float timestamp, or 0.0 if decoding fails.
        """
        try:
            import base64
            import json
            parts = token.split('.')
            if len(parts) == 3:
                payload = base64.urlsafe_b64decode(parts[1] + '==')
                data = json.loads(payload)
                return float(data.get('exp', 0.0))
        except Exception as e:
            print(f"Error decoding token for expiry: {e}")
        return 0.0

    def get_id_token(self) -> str:
        """Get an ID token to authenticate with the MCP server with local fallback and caching.

        Retrieval order:
        1. In-memory cache (if valid).
        2. LOCAL_GCP_ID_TOKEN environment override.
        3. Standard GCP library authentication.
        4. Fallback gcloud print-identity-token.

        Returns:
            The ID token string.

        Raises:
            Exception: If all retrieval methods fail.
        """
        import time
        current_time = time.time()
        
        # 1. Check if valid cached token exists
        if self._cached_token and current_time < self._cached_token_expiry - 60: # 1 min buffer
            remain = self._cached_token_expiry - current_time
            print(f"Using cached ID token. Valid for {int(remain)} more seconds.")
            return self._cached_token

        print("getting id token...")
        target_url = os.getenv("MCP_SERVER_URL")
        if not target_url:
             raise Exception("MCP_SERVER_URL environment variable not set.")
        audience = target_url.split('/mcp/')[0]

        # 2. Check for manual override in .env
        local_token = os.getenv("LOCAL_GCP_ID_TOKEN")
        if local_token:
            print("Using local token override from environment.")
            self._cached_token = local_token
            self._cached_token_expiry = current_time + 3000 # 50 mins
            return local_token

        # 3. Try standard GCP method
        retrieved_token = None
        try:
            request = google.auth.transport.requests.Request()
            retrieved_token = google.oauth2.id_token.fetch_id_token(request, audience)
        except Exception as e:
            print(f"Standard ID token retrieval failed: {e}. Trying fallback...")

        # 4. Try subprocess gcloud print-identity-token as fallback
        if not retrieved_token:
            retrieved_token = self._get_id_token_via_gcloud(audience)

        if retrieved_token:
            self._cached_token = retrieved_token
            self._cached_token_expiry = self._get_token_expiry(retrieved_token)
            if self._cached_token_expiry == 0.0:
                 # Fallback if expiry decoding fails
                 self._cached_token_expiry = current_time + 3000 # 50 mins
            return retrieved_token

        raise Exception("Failed to retrieve ID token from all methods.")

    def get_gcp_auth_header(self, tool_context: ToolContext) -> Dict[str, Any]:
        """Provides the Authorization header with a Bearer token for GCP MCP server.

        Args:
            tool_context: The ADK ToolContext (unused but required by signature).

        Returns:
            A dictionary containing the Authorization header.
        """
        token = self.get_id_token()
        return {"Authorization": f"Bearer {token}"}

    def get_azure_auth_header(self, tool_context: ToolContext) -> Dict[str, Any]:
        """Provides the x-functions-key header for Azure MCP server.

        Args:
            tool_context: The ADK ToolContext (unused but required by signature).

        Returns:
            A dictionary containing the x-functions-key header.
        """
        azure_key = os.getenv("AZURE_MCP_SERVER_KEY")
        return {"x-functions-key": azure_key or ""}

# Create a singleton instance
token_manager = TokenManager()
