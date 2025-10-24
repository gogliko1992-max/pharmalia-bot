# file: pharmalia_webhook.py
import os
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

CITY, SERVICE, NAME, PHONE = range(4)

# 🔹 Токен вставлен напрямую
BOT_TOKEN = "8396406613:AAEOcf1M88KuCYVjpVKT_XmHePCKLGwVz60"
ADMIN_CHAT_ID = "@Pharmalia"  # ID или username администратора/группы

# Создаём приложение Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Батуми"]]
    await update.message.reply_text(
        "Здравствуйте! Для начала выберите город:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["city"] = update.message.text
    reply_keyboard = [
        ["Вакцинация", "Педиатрия"],
        ["Реабилитация", "Лаборатория"],
        ["УЗИ"],
    ]
    await update.message.reply_text(
        "Какую услугу вы хотите выбрать?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return SERVICE

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["service"] = update.message.text
    await update.message.reply_text(
        "Чтобы записаться, напишите своё имя:", reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("И свой грузинский номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text
    info = context.user_data
    admin_msg = (
        f"Новая запись в клинику Фармалиа\n"
        f"Город: {info['city']}\n"
        f"Услуга: {info['service']}\n"
        f"Имя: {info['name']}\n"
        f"Телефон: {info['phone']}"
    )
    await application.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
    await update.message.reply_text(
        "Спасибо! Наш сотрудник свяжется с вами в ближайшее время. Нажмите /start, чтобы записаться снова."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Запись отменена. Если хотите начать заново, отправьте /start.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

# Регистрируем обработчики
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
        SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
application.add_handler(conv_handler)

# Flask-приложение для приёма веб-хуков
app = Flask(__name__)

@app.post("/")
async def webhook_handler():
    """Обработчик входящих обновлений от Telegram."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"

if __name__ == "__main__":
    # При локальном запуске используем встроенный веб-сервер Flask
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

