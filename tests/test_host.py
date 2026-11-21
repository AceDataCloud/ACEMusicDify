from unittest import TestCase
from unittest.mock import patch

from dify_plugin import DifyPluginEnv
from dify_plugin.core.plugin_registration import PluginRegistration
from dify_plugin.entities.tool import ToolRuntime


class HostTest(TestCase):
    def test_real_sdk_resolves_nine_tools_and_dispatches_query(self):
        registry = PluginRegistration(DifyPluginEnv())
        self.assertEqual(len(registry.tools_mapping["acemusic"][2]), 9)
        tool_cls = registry.get_tool_cls("acemusic", "acemusic_retrieve")
        runtime = ToolRuntime(
            credentials={"acedata_bearer_token": "fixture"},
            user_id=None,
            session_id=None,
        )
        tool = tool_cls(runtime, None)
        result = {"id": "saved", "state": "pending"}
        with patch("client.requests.post") as post:
            post.return_value.status_code = 200
            post.return_value.json.return_value = result
            messages = list(tool._invoke({"task_id": "saved"}))
        self.assertEqual(messages[0].message.json_object, result)
        self.assertEqual(
            post.call_args.kwargs["json"], {"action": "retrieve", "id": "saved"}
        )
