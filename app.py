import asyncio
from flask import Flask, request
from telegram.ext import Application
from bot import application  # Это твой telegram Application
import os

app = Flask(__name__)

# Инициализация Telegram Application
@app.before_first_request
def initialize_telegram():
    loop = asyncio.get_event_loop()
    if not application._initialized:
        loop.run_until_complete(application.initialize())
        print("✅ Telegram Application initialized.")

# Webhook endpoint
@app.route(f"/{os.environ['BOT_TOKEN']}", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True)
    application.update_queue.put_nowait(update)
    return "OK", 200

# Для проверки, что сайт работает
@app.route("/", methods=["GET"])
def home():
    return "NZ Immigration Lawyer Bot is running!", 200
