# WebExBot

A small FastAPI-based Webex bot for sending human-in-the-loop approval requests as adaptive cards and receiving webhook events when a user interacts with those cards.

## What this project does

This project lets you:

- send a structured approval request to a Webex user via an adaptive card
- include ticket metadata such as title, priority, status, confidence, analysis, and execution plan
- receive Webex attachment action events through a webhook endpoint
- create and manage Webex webhooks for attachment actions

## Project structure

- [main.py](main.py) — FastAPI app with endpoints for sending messages and receiving webhook callbacks
- [bot_script.py](bot_script.py) — Webex API helpers for looking up users, sending approval requests, creating webhooks, and fetching attachment actions
- [create_webhook.py](create_webhook.py) — example script for creating a webhook against a public callback URL
- [card.json](card.json) — the adaptive card template used in approval requests
- [pyproject.toml](pyproject.toml) — project dependencies and Python version

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A Webex bot token stored in your environment

## Setup

1. Create a `.env` file in the project root with your Webex bot token and recepient email. There should be an account in webex for this email:

   ```env
   BOT_TOKEN=your_webex_bot_token
   RECEPIENT_EMAIL=email@emai.com
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Start the FastAPI app:

   ```bash
   uv run fastapi dev main.py
   ```

## API endpoints

### GET /

Returns a simple health-style response:

```json
{"message": "Hello World"}
```

### POST /send_message

Sends an approval request to a configured Webex user.

Request body:

```json
{
  "message": "Please review this ticket",
  "ticket_id": "INC-1001",
  "title": "Server outage",
  "priority": "High",
  "status": "Open",
  "confidence": 95,
  "analysis": "Root cause identified",
  "resolution": "Restart services",
  "execution_plan": "Validate after restart"
}
```


### POST /webhook

Receives Webex attachment action webhook events and prints the response payload.

## Webhook setup

Before using the webhook flow, update [create_webhook.py](create_webhook.py) with a reachable public URL for your app.

Run:

```bash
uv run python create_webhook.py
```

This creates a Webex webhook for `attachmentActions` events.

## Notes

- The adaptive card template in [card.json](card.json) uses placeholders such as `{{ticket_id}}` and `{{title}}`.
- The request payload values are substituted into the card before it is sent to Webex.
- This project is intended for a simple approval workflow and can be extended for richer bot interactions.
