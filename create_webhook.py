from bot_script import create_webhook

response = create_webhook(
    "https://c6080771904b9f.lhr.life/webhook"
)
print(response.json())
