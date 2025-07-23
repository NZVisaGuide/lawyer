from flask import Flask, request
from telegram import Update
from bot import application  # Telegram Application, собранный в bot.py
import os
import asyncio

app = Flask(__name__)

BOT_TOKEN = os.environ['BOT_TOKEN']

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)

    asyncio.run(application.process_update(update))

    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "NZ Immigration Lawyer Bot is running!", 200

# 👇 Добавь этот блок обязательно
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
