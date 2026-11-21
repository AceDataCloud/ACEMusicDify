import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from client import build_request, invoke


class ContractTests(TestCase):
    def test_wire_contract_for_every_operation(self):
        cases = json.loads(Path(__file__).with_name("requests.json").read_text())
        for name, (inputs, expected) in cases.items():
            with self.subTest(operation=name):
                self.assertEqual(list(build_request(name, inputs)), expected)

    def test_invalid_references_rejected_before_network(self):
        with self.assertRaises(ValueError):
            build_request(
                "mashup",
                {
                    "first_audio_id": "a",
                    "second_audio_id": "a",
                    "style": "folk",
                    "lyric": "verse",
                },
            )

    @patch("client.requests.post")
    def test_preserve_partial_result_and_original_task(self, post):
        result = {
            "id": "t1",
            "response": {
                "status": "partial_failed",
                "data": [{"audio_url": "https://media.example/song.mp3"}],
            },
        }
        post.return_value.status_code = 200
        post.return_value.json.return_value = result
        self.assertEqual(invoke("fixture", "retrieve", {"task_id": "t1"}), result)
        post.assert_called_once()
        args, kwargs = post.call_args
        self.assertEqual(args, ("https://api.acedata.cloud/acemusic/tasks",))
        self.assertEqual(kwargs["json"], {"action": "retrieve", "id": "t1"})
        self.assertFalse(kwargs["allow_redirects"])
