from typing import Any
import requests

from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider

class GPUStackProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        base_url = credentials.get("base_url", "").removesuffix("/").removesuffix("/v1").removesuffix("/v1-openai")
        api_key = credentials.get("api_key", "")
        tls_verify = bool(credentials.get("tls_verify", True))

        if not base_url:
            raise ToolProviderCredentialValidationError("GPUStack base_url is required")
        if not api_key:
            raise ToolProviderCredentialValidationError("GPUStack api_key is required")
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {api_key}",
        }

        response = requests.get(f"{base_url}/v1/models", headers=headers, verify=tls_verify)
        if response.status_code != 200:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate GPUStack API key, status code: {response.status_code}-{response.text}"
            )
