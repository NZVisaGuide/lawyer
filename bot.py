from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from config import BOT_TOKEN
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Шаги формы
FULLNAME, RESIDENCE, PHONE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("New Zealand", callback_data="New Zealand")],
        [InlineKeyboardButton("Australia", callback_data="Australia")],
        [InlineKeyboardButton("Canada", callback_data="Canada")]
    ]
    await update.message.reply_text(
        "Здравствуйте! Пожалуйста, выберите страну:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    context.user_data['country'] = country
    await query.answer()

    stripe_url = "https://buy.stripe.com/test_examplelink"  # Заменить на реальный Stripe-ссылка
    keyboard = [[InlineKeyboardButton("💳 Оплатить через Stripe", url=stripe_url)]]

    await query.edit_message_text(
        text=f"Вы выбрали: {country}.\n\n💳 Пожалуйста, оплатите консультацию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await context.bot.send_message(chat_id=query.message.chat_id, text="После оплаты нажмите /continue")

async def continue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, введите ваше полное имя:")
    return FULLNAME

async def get_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fullname"] = update.message.text
    await update.message.reply_text("Введите вашу страну проживания:")
    return RESIDENCE

async def get_residence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["residence"] = update.message.text
    await update.message.reply_text("Введите ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    fullname = context.user_data.get("fullname")
    residence = context.user_data.get("residence")
    phone = context.user_data.get("phone")
    country = context.user_data.get("country", "Не выбрана")

    message = (
        f"📝 Новая заявка:\n\n"
        f"🌍 Выбранная страна: {country}\n"
        f"👤 ФИО: {fullname}\n"
        f"🏠 Страна проживания: {residence}\n"
        f"📞 Телефон: {phone}"
    )

    await update.message.reply_text("Спасибо! Ваши данные отправлены. Мы свяжемся с вами в ближайшее время.")

    # Отправка на email
    send_email(message)
    return ConversationHandler.END

def send_email(message: str):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER
    msg["Subject"] = "Новая заявка от Telegram-бота"

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Форма отменена.")
    return ConversationHandler.END

# Создание приложения Telegram
application = Application.builder().token(BOT_TOKEN).build()

form_conversation = ConversationHandler(
    entry_points=[CommandHandler("continue", continue_command)],
    states={
        FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fullname)],
        RESIDENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_residence)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(country_selected))
application.add_handler(form_conversation)

if __name__ == "__main__":
    application.run_polling()
