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
   uv run fastapi dev main.py --host 0.0.0.0 --port 8000
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

Webex must be able to reach the local FastAPI application's `/webhook` endpoint. Use `localhost.run` to create a public HTTPS tunnel to the app running on port `8000`.

1. In a separate terminal, from the project directory, create the tunnel:

   ```bash
   ssh -R 80:localhost:8000 localhost.run
   ```

2. Leave the SSH session running. It prints a public URL similar to `https://example.lhr.life`. Copy this URL.

3. Update [create_webhook.py](create_webhook.py) with the copied tunnel URL followed by `/webhook`:

   ```python
   response = create_webhook(
       "https://example.lhr.life/webhook"
   )
   ```

   The `https://` scheme and `/webhook` path are both required.

4. Create the Webex webhook:

```bash
uv run python create_webhook.py
```

This creates a Webex webhook for `attachmentActions` events. Keep both the FastAPI server and the tunnel running while testing card actions. `localhost.run` URLs can change when a new tunnel is created, so update the webhook callback URL and recreate the Webex webhook when that happens.

## Notes

- The adaptive card template in [card.json](card.json) uses placeholders such as `{{ticket_id}}` and `{{title}}`.
- The request payload values are substituted into the card before it is sent to Webex.
- This project is intended for a simple approval workflow and can be extended for richer bot interactions.
