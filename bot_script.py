import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN","")

headers = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}


def get_person_id(email: str):
    response = requests.get(
        f"https://webexapis.com/v1/people?email={email}",
        headers=headers
    )
    print(response.status_code)
    return response.json().get("items", [{}])[0].get("id", None)


def send_approval_request(person_id: str, message: str, ticket: dict):
    print("*"*40)
    print(f"Sending approval request to person_id: {person_id} with message: {message} and ticket: {ticket}")
    print("*"*40)
    
    with open("card.json", "r") as f:
        card = json.load(f)

    card_str = json.dumps(card)

    for key, value in ticket.items():
        card_str = card_str.replace(f"{{{{{key}}}}}", str(value))

    card = json.loads(card_str)

    payload = {
        "toPersonId": person_id,
        "markdown": message,
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card
            }
        ]
    }

    return requests.post(
        "https://webexapis.com/v1/messages",
        headers=headers,
        json=payload
    )




import requests

WEBEX_API = "https://webexapis.com/v1"

headers = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

def create_webhook(target_url: str):
    payload = {
        "name": "HITL Approval Webhook",
        "targetUrl": target_url,
        "resource": "attachmentActions",
        "event": "created"
    }

    response = requests.post(
        f"{WEBEX_API}/webhooks",
        headers=headers,
        json=payload
    )

    print("*"*40)
    print(f"Creating webhook with target URL: {target_url}")
    print("*"*40)


    return response


def list_webhooks():
    return requests.get(
        f"{WEBEX_API}/webhooks",
        headers=headers
    )

def delete_webhook(webhook_id: str):
    return requests.delete(
        f"{WEBEX_API}/webhooks/{webhook_id}",
        headers=headers
    )




def get_attachment_action(action_id: str):
    response = requests.get(
        f"https://webexapis.com/v1/attachment/actions/{action_id}",
        headers=headers
    )

    return response