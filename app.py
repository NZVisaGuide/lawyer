from flask import Flask
from stripe_payment import stripe_bp
from bot import application
import asyncio
import threading

app = Flask(__name__)
app.register_blueprint(stripe_bp)

# Запуск Telegram-бота в фоне вручную (async)
def run_telegram_bot():
    async def start_bot():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
    
    asyncio.run(start_bot())

threading.Thread(target=run_telegram_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
