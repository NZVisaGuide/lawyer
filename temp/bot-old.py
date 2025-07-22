import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
import smtplib
from email.mime.text import MIMEText

# Логгирование
logging.basicConfig(level=logging.INFO)

# Состояния для ConversationHandler
GET_NAME, GET_LIVE_COUNTRY = range(2)

# Старт бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("New Zealand", callback_data="New Zealand")],
        [InlineKeyboardButton("Australia", callback_data="Australia")],
        [InlineKeyboardButton("Canada", callback_data="Canada")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Здравствуйте! Пожалуйста, выберите страну для консультации:", reply_markup=reply_markup)

# Выбор страны
async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    context.user_data['country'] = country
    await query.answer()

    await query.edit_message_text(
        text=f"Вы выбрали: {country}.\n\n💳 Пожалуйста, перейдите к оплате по ссылке ниже:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оплатить 100 NZD", url="https://your-payment-link.com")]
        ])
    )

    await context.bot.send_message(chat_id=query.message.chat_id, text="После оплаты нажмите /continue")

# Команда /continue
async def start_data_collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваше ФИО:")
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Укажите страну вашего проживания:")
    return GET_LIVE_COUNTRY

async def get_live_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['live_country'] = update.message.text

    # Отправка данных на email
    send_email(
        name=context.user_data['name'],
        selected_country=context.user_data['country'],
        live_country=context.user_data['live_country']
    )

    await update.message.reply_text("Спасибо! Мы получили ваши данные. Адвокат свяжется с вами в Telegram.")
    return ConversationHandler.END

# Отправка email
def send_email(name, selected_country, live_country):
    body = f"""Новая заявка на консультацию:
ФИО: {name}
Выбранная страна: {selected_country}
Страна проживания: {live_country}
"""

    msg = MIMEText(body)
    msg['Subject'] = 'Новая заявка'
    msg['From'] = 'yourbot@gmail.com'
    msg['To'] = 'nzadvocat@gmail.com'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('yourbot@gmail.com', 'your_app_password')  # Вставь здесь App Password!
        smtp.send_message(msg)

# Главная функция
def main():
    app = ApplicationBuilder().token("7770078456:AAHC411S5upMBRLkHY1GixA0JBGtqWYRs2I").build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(country_selected))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("continue", start_data_collection)],
        states={
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_LIVE_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_live_country)],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
