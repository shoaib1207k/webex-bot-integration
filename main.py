from fastapi import FastAPI, Request, status
import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from bot_script import get_attachment_action, get_person_name

load_dotenv()

# RECPIENT_EMAIL = os.getenv("RECPIENT_EMAIL")
# RECPIENT_EMAIL = "vipuluniyal16@gmail.com"
RECPIENT_EMAIL = "shoaib1207k@gmail.com"
RECPIENT_EMAIL = "shoaib12dev@gmail.com"
# RECPIENT_EMAIL = "softer.vishalgoel@gmail.com"





class TicketApprovalRequest(BaseModel):
    message: str
    ticket_id: str
    title: str
    priority: str
    status: str
    confidence: int
    analysis: str
    resolution: str
    execution_plan: str

# Initialize the FastAPI application instance
app = FastAPI()

# Define a root path operation
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/send_message", status_code=status.HTTP_200_OK)
def send_message(message: str):
    from bot_script import send_message, get_person_id

    email = RECPIENT_EMAIL
    person_id = get_person_id(email)

    print(email)
    print(person_id)

    if not person_id:
        return {"error": "Person not found"}

    response = send_message(
        person_id=person_id,
        message=message
    )

    return response.json()

@app.post("/send_approval_request", status_code=status.HTTP_200_OK)
def send_approval_request(request: TicketApprovalRequest):
    from bot_script import send_approval_request, get_person_id

    email = RECPIENT_EMAIL
    print(email)
    person_id = get_person_id(email)
    print(person_id)
    if not person_id:
        return {"error": "Person not found"}

    response = send_approval_request(
        person_id=person_id,
        message=request.message,
        ticket=request.model_dump()
    )

    return response.json()


@app.post("/webhook")
async def webex_webhook(request: Request):
    payload = await request.json()

    action_id = payload["data"]["id"]
    response = get_attachment_action(action_id)
    attachment_action = response.json()
    person_id = attachment_action.get("personId")
    person_name = get_person_name(person_id) if person_id else None
    inputs = attachment_action.get("inputs", {})

    print(json.dumps({
        "personId": person_id,
        "personName": person_name,
        "action": inputs.get("action"),
        "ticketId": inputs.get("ticketId"),
        "reviewComments": inputs.get("reviewComments"),
    }, indent=4))
    
    return {"status": "ok"}


@app.post("/list-webhooks")
def list_webhooks():
    from bot_script import list_webhooks
    
    response = list_webhooks()

    return response.json()

@app.post("/delete-webhook")
def delete_webhook(webhook_id: str):
    from bot_script import delete_webhook
    
    response = delete_webhook(webhook_id)

    return {
        "success": response.status_code== 204 ,
        "status_code": response.status_code
    }