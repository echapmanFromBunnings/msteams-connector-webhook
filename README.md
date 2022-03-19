# Microsoft Teams Webhook Notifications

This actions sends a message to your Microsoft Teams channel using an Incoming Webhook connector. An Incoming Webhook connector must be setup on your Microsoft Teams channel before this action can be used successfully.

[Get started with Microsoft Teams Connectors Incoming Webhook](https://medium.com/@ankush.kumar133/get-started-with-microsoft-team-connectors-incoming-webhook-a330657993e7)

## Inputs

### `webhook`

**Required** The webhook url for your Incoming Webhook connector.

### `title`

**Required** The title for the message you want to send to your Microsoft Teams channel.

### `message`

**Required** The message you want to send to your Microsoft Teams channel.

## Example usage

```
- name: Send message to ms teams
  uses: echapmanFromBunnings/msteams-connector-webhook@1.0
  with:
    webhook: 'https://outlook.office.com/webhook/<webHookId>'
    message: 'Hello world. This is a slug... &#x1F41B;'
```
