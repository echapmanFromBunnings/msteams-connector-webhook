#!/usr/bin/env python3
"""Send an Adaptive Card to a Microsoft Teams / Power Automate webhook.

This replaces the legacy Office 365 Connector MessageCard format with the
Adaptive Card format required by Power Automate "Post card in a chat or
channel" workflows.
"""

import argparse
import json
import sys

import requests


def build_payload(title: str, message: str) -> dict:
    """Build the Teams/Power Automate Adaptive Card payload."""
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "msTeams": {"width": "full"},
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": title,
                            "wrap": True,
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True,
                        },
                    ],
                },
            }
        ],
    }


def send_card(webhook_url: str, title: str, message: str) -> requests.Response:
    """POST the Adaptive Card payload to the webhook URL."""
    payload = build_payload(title, message)
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        webhook_url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30,
    )
    response.raise_for_status()
    return response


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Send an Adaptive Card to a Microsoft Teams / Power Automate webhook"
    )
    parser.add_argument("webhook", help="Webhook URL")
    parser.add_argument("title", help="Card title")
    parser.add_argument("message", help="Card message")
    parser.add_argument(
        "--dump",
        action="store_true",
        help="Print the JSON payload instead of sending it",
    )
    args = parser.parse_args(argv)

    if args.dump:
        print(json.dumps(build_payload(args.title, args.message), indent=2))
        return 0

    try:
        response = send_card(args.webhook, args.title, args.message)
        print(f"Message sent successfully. Status: {response.status_code}")
        return 0
    except requests.exceptions.RequestException as exc:
        print(f"Failed to send message: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
