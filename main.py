from fastapi import FastAPI, Request, status
import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from bot_script import get_attachment_action

load_dotenv()

RECPIENT_EMAIL = os.getenv("RECPIENT_EMAIL")
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
def send_message(request: TicketApprovalRequest):
    from bot_script import send_approval_request, get_person_id

    email = RECPIENT_EMAIL
    person_id = get_person_id(email)

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

    print(json.dumps(response.json(), indent=4))
    
    return {"status": "ok"}