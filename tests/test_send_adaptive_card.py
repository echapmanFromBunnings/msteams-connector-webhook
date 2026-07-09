"""Unit tests for the Adaptive Card sender."""

import json
import unittest
from unittest import mock

import requests

from send_adaptive_card import build_payload, main, send_card


class BuildPayloadTests(unittest.TestCase):
    def test_payload_structure(self):
        payload = build_payload("My Title", "My message body")

        self.assertEqual(payload["type"], "message")
        self.assertEqual(len(payload["attachments"]), 1)

        attachment = payload["attachments"][0]
        self.assertEqual(
            attachment["contentType"], "application/vnd.microsoft.card.adaptive"
        )
        self.assertIsNone(attachment["contentUrl"])

        card = attachment["content"]
        self.assertEqual(card["type"], "AdaptiveCard")
        self.assertEqual(card["version"], "1.4")
        self.assertEqual(card["msTeams"]["width"], "full")
        self.assertEqual(len(card["body"]), 2)
        self.assertEqual(card["body"][0]["text"], "My Title")
        self.assertEqual(card["body"][1]["text"], "My message body")

    def test_special_characters_are_preserved(self):
        payload = build_payload("Título", "Mensaje con emojis 🐛")
        body = payload["attachments"][0]["content"]["body"]
        self.assertEqual(body[0]["text"], "Título")
        self.assertEqual(body[1]["text"], "Mensaje con emojis 🐛")


class SendCardTests(unittest.TestCase):
    @mock.patch("send_adaptive_card.requests.post")
    def test_send_card_posts_json(self, mock_post):
        mock_post.return_value.status_code = 202
        mock_post.return_value.raise_for_status = mock.Mock()

        send_card("https://example.com/webhook", "Title", "Message")

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://example.com/webhook")
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")

        posted = json.loads(kwargs["data"])
        self.assertEqual(posted["type"], "message")
        self.assertEqual(
            posted["attachments"][0]["content"]["body"][0]["text"], "Title"
        )

    @mock.patch("send_adaptive_card.requests.post")
    def test_send_card_raises_on_failure(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = requests.HTTPError("boom")

        with self.assertRaises(requests.HTTPError):
            send_card("https://example.com/webhook", "Title", "Message")


class MainTests(unittest.TestCase):
    @mock.patch("send_adaptive_card.requests.post")
    def test_main_exits_zero_on_success(self, mock_post):
        mock_post.return_value.status_code = 202
        mock_post.return_value.raise_for_status = mock.Mock()

        result = main(["https://example.com/webhook", "Title", "Message"])

        self.assertEqual(result, 0)

    @mock.patch("send_adaptive_card.requests.post")
    def test_main_exits_non_zero_on_failure(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = requests.HTTPError("boom")

        result = main(["https://example.com/webhook", "Title", "Message"])

        self.assertEqual(result, 1)

    def test_main_dump_prints_payload(self):
        with mock.patch("builtins.print") as mock_print:
            result = main(["https://example.com/webhook", "Title", "Message", "--dump"])

        self.assertEqual(result, 0)
        printed = "\n".join(call.args[0] for call in mock_print.call_args_list)
        self.assertIn("AdaptiveCard", printed)


if __name__ == "__main__":
    unittest.main()
