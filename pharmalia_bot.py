import os
from flask import Flask, request
import requests

app = Flask(__name__)

# 🔐 Твой токен
BOT_TOKEN = "8396406613:AAEOcf1M88KuCYVjpVKT_XmHePCKLGwVz60"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "✅ Pharmalia bot is running on Google Cloud!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    # ✅ Когда в группу добавляется новый человек
    if "message" in data and "new_chat_members" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        new_users = data["message"]["new_chat_members"]

        for user in new_users:
            name = user.get("first_name", "друг")
            welcome_text = (
                f"👋 Привет, {name}!\n\n"
                "Добро пожаловать в клинику *Фармалия* 💙\n"
                "🏥 Мы находимся по адресу: Вахтанг Горгасали тупик 4, Батуми.\n\n"
                "💉 Если вы в Батуми — вакцинация *первые 3 месяца бесплатно*.\n"
                "💬 Консультация врача — *70 лари*.\n"
                "📄 Медицинская форма 100 — *30 лари*.\n"
                "🧠 У нас работает *реабилитационный центр*, доступны *УЗИ*, лабораторные анализы и терапевтические услуги.\n\n"
                "🕓 График работы:\n"
                "Понедельник – Суббота: *09:00 – 20:00*\n"
                "Воскресенье – выходной.\n\n"
                "Нажмите кнопку ниже, чтобы записаться 👇"
            )

            # 📲 Кнопка для записи по номеру телефона
            button = {
                "inline_keyboard": [
                    [{"text": "📲 Записаться", "url": "https://t.me/+995593509357"}]
                ]
            }

            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": welcome_text,
                "parse_mode": "Markdown",
                "reply_markup": button
            })

    return "ok", 200
