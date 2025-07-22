from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("New Zealand", callback_data="New Zealand")],
        [InlineKeyboardButton("Australia", callback_data="Australia")],
        [InlineKeyboardButton("Canada", callback_data="Canada")]
    ]
    await update.message.reply_text("Здравствуйте! Пожалуйста, выберите страну:", reply_markup=InlineKeyboardMarkup(keyboard))

async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    country = query.data
    context.user_data['country'] = country
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("💰 PayPal", url="https://www.paypal.com/paypalme/yourusername"),
            InlineKeyboardButton("💳 Stripe", url="https://buy.stripe.com/test_examplelink"),
            InlineKeyboardButton("🇺🇦 WayForPay", url="https://secure.wayforpay.com/pay/yourpaymentlink")
        ]
    ]

    await query.edit_message_text(
        text=f"Вы выбрали: {country}.\n\n💳 Пожалуйста, выберите способ оплаты:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await context.bot.send_message(chat_id=query.message.chat_id, text="После оплаты нажмите /continue")

# Создание приложения Telegram
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(country_selected))
