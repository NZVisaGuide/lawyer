import os
import asyncio
from flask import Flask, request
from bot import application, BOT_TOKEN
from config import WEBHOOK_URL
from stripe_payment import stripe_bp



app = Flask(__name__)
app.register_blueprint(stripe_bp)

@app.route('/')
def index():
    return "Bot is running."

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json(force=True)
    asyncio.run(application.process_update(update))
    return "ok", 200

# ---- Устанавливаем webhook при запуске ----
async def setup_webhook():
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

if __name__ == '__main__':
    asyncio.run(setup_webhook())
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
