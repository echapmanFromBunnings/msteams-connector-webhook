# Microsoft Teams Incoming Webhook Notifications

This action sends a message to your Microsoft Teams channel using a **Power Automate** workflow webhook. It posts the message as an [Adaptive Card](https://adaptivecards.io/), which is the format required by modern Teams workflows created in Power Apps / Power Automate.

> **Note:** Legacy Office 365 Connector webhooks are deprecated. Create a "Post card in a chat or channel" Power Automate workflow and paste its webhook URL into the `webhook` input.

[Create a Power Automate Teams workflow](https://learn.microsoft.com/en-us/power-automate/create-team-flows)

## Inputs

The action surface area is unchanged; only the backend payload format has changed.

### `webhook`

**Required** The webhook URL for your Power Automate "Post card in a chat or channel" workflow.

### `title`

**Required** The title displayed on the Adaptive Card.

### `message`

**Required** The message body displayed on the Adaptive Card.

## Example usage

```yaml
- name: Send message to ms teams channel
  uses: echapmanFromBunnings/msteams-connector-webhook@2.0.3
  with:
    webhook: 'https://<region>.webhook.office.com/webhookb2/<tenant>/IncomingWebhook/<id>/<guid>'
    title: 'Deployment started'
    message: 'Hello world. This is a slug... &#x1F41B;'
```

## Testing

Install Python dependencies first:

```bash
pip install -r requirements.txt
```

- Python test harness: `python -m unittest discover tests`
- Validate payload locally: `tests/Validate-AdaptiveCardPayload.ps1`
- Send a test card: `tests/Send-TestAdaptiveCard.ps1 -WebhookUrl '<url>' -Title 'Test' -Message 'Hello'`
