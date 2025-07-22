from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это бот иммиграционного юриста.")

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
