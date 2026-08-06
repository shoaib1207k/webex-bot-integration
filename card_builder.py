from typing import Dict, Any


def build_hitl_card(ticket: Dict[str, Any], title: str, priority: str, requester: str | None = None) -> Dict[str, Any]:
    """Build an adaptive card matching card.json structure used by the POC.

    Expects ticket keys: ticket_id, title, priority, status, confidence, analysis, resolution, execution_plan
    """
    facts = [
        {"title": "Ticket ID", "value": ticket.get("ticket_id", "")},
        {"title": "Title", "value": ticket.get("title", "")},
        {"title": "Priority", "value": ticket.get("priority", priority)},
        {"title": "Status", "value": ticket.get("status", "")},
        {"title": "Confidence", "value": f"{ticket.get('confidence','')}%"},
    ]

    body = [
        {
            "type": "TextBlock",
            "text": "🤖 AI Resolution Approval",
            "size": "Large",
            "weight": "Bolder",
            "color": "Accent",
        },
        {
            "type": "TextBlock",
            "text": "Please review the AI-generated resolution before execution.",
            "wrap": True,
            "spacing": "Small",
        },
        {"type": "FactSet", "facts": facts},
        {"type": "TextBlock", "text": "### AI Analysis", "weight": "Bolder", "spacing": "Medium"},
        {"type": "Container", "style": "emphasis", "items": [{"type": "TextBlock", "text": ticket.get("analysis", ""), "wrap": True}]},
        {"type": "TextBlock", "text": "### Proposed Resolution", "weight": "Bolder", "spacing": "Medium"},
        {"type": "Container", "style": "emphasis", "items": [{"type": "TextBlock", "text": ticket.get("resolution", ""), "wrap": True}]},
        {"type": "TextBlock", "text": "### Planned Actions", "weight": "Bolder", "spacing": "Medium"},
        {"type": "Container", "style": "emphasis", "items": [{"type": "TextBlock", "text": ticket.get("execution_plan", ""), "wrap": True}]},
        {"type": "Input.Text", "id": "reviewComments", "placeholder": "Optional comments...", "isMultiline": True},
    ]

    actions = [
        {
            "type": "Action.Submit",
            "title": "✅ Approve",
            "data": {"action": "approve", "ticketId": ticket.get("ticket_id")},
        },
        {
            "type": "Action.Submit",
            "title": "❌ Reject",
            "data": {"action": "reject", "ticketId": ticket.get("ticket_id")},
        },
    ]

    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": body,
            "actions": actions,
        },
    }

    return attachment
