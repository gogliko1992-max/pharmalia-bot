import os
from flask import Flask, request
import requests

# --- Настройки ---
BOT_TOKEN = "8396406613:AAEOcf1M88KuCYVjpVKT_XmHePCKLGwVz60"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_PATH = f"/{BOT_TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ Pharmalia bot is running on Google Cloud!", 200

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "no data", 400

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if chat_id and text:
        reply = "Здравствуйте 👋 Это бот клиники *Pharmalia*.\n\n📅 Для записи нажмите 👉 @Pharmalia"
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
        })

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
