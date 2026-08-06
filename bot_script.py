import os
import json
from dotenv import load_dotenv
load_dotenv()
from card_builder import build_hitl_card
from webex_client import WebexClient

BOT_TOKEN = os.getenv("BOT_TOKEN", "")


def _client() -> WebexClient:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set in environment")
    return WebexClient(BOT_TOKEN)


def get_person_id(email: str):
    client = _client()
    resp = client.get(f"/people?email={email}")
    print(resp.status_code)
    resp.raise_for_status()
    people = resp.json().get("items", [])
    return people[0].get("id") if people else None


def get_person_name(person_id: str) -> str | None:
    client = _client()
    resp = client.get(f"/people/{person_id}")
    resp.raise_for_status()
    return resp.json().get("displayName")


def send_message(person_id: str, message: str):
    client = _client()
    payload = {
        "toPersonId": person_id,
        "markdown": message,
    }
    resp = client.post("/messages", json=payload)
    return resp


def send_approval_request(person_id: str, message: str, ticket: dict):
    print("*"*40)
    print(f"Sending approval request to person_id: {person_id} with message: {message} and ticket: {ticket}")
    print("*"*40)

    # Build attachment programmatically
    attachment = build_hitl_card(ticket, title=ticket.get("title", "Approval Request"), priority=ticket.get("priority", ""), requester=ticket.get("requester"))
    payload = {
        "toPersonId": person_id,
        "markdown": message,
        "attachments": [attachment],
    }

    client = _client()
    resp = client.post("/messages", json=payload)
    return resp




WEBEX_API = "/webhooks"


def create_webhook(target_url: str):
    client = _client()
    payload = {
        "name": "HITL Approval Webhook",
        "targetUrl": target_url,
        "resource": "attachmentActions",
        "event": "created",
    }
    resp = client.post(WEBEX_API, json=payload)
    print("*"*40)
    print(f"Creating webhook with target URL: {target_url}")
    print("*"*40)
    return resp


def list_webhooks():
    client = _client()
    return client.get("/webhooks")


def delete_webhook(webhook_id: str):
    client = _client()
    return client.delete(f"/webhooks/{webhook_id}")



def get_attachment_action(action_id: str):
    client = _client()
    return client.get(f"/attachment/actions/{action_id}")