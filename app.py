from flask import Flask, request
from config import BOT_TOKEN, WEBHOOK_URL
from bot import application

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running."

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = application.bot._extract_update(request.get_json(force=True))
    application.process_update(update)
    return "ok"

if __name__ == "__main__":
    application.bot.delete_webhook()
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(port=8080)
