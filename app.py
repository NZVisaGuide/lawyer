import asyncio
from flask import Flask, request
from telegram.ext import Application
from bot import application  # Telegram Application
import os

app = Flask(__name__)
initialized = False  # Флаг инициализации

@app.route(f"/{os.environ['BOT_TOKEN']}", methods=["POST"])
def telegram_webhook():
    global initialized
    if not initialized:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.initialize())
        initialized = True
        print("✅ Telegram Application initialized.")

    update = request.get_json(force=True)
    application.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "NZ Immigration Lawyer Bot is running!", 200
