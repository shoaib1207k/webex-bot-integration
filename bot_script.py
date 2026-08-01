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

