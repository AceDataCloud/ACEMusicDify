from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from client import invoke


class AceMusicProvider(ToolProvider):
    def _validate_credentials(self, credentials):
        try:
            invoke(
                credentials.get("acedata_bearer_token"),
                "history",
                {"page": 1, "page_size": 1},
            )
        except (ValueError, RuntimeError) as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from None
