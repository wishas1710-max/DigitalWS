from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с сайта

# НАСТРОЙКИ ТЕЛЕГРАМ БОТА
TOKEN = "8717286736:AAEJMk57rXGCf8Em_IzkKLlputNZZ_ZcRAU"
CHAT_ID = "-1003953924346"

@app.route('/api/order', methods=['POST'])
def receive_order():
    data = request.json
    service = data.get('service')
    name = data.get('name')
    contact = data.get('contact')
    comment = data.get('comment', 'Нет комментария')

    # Формируем красивое сообщение для Telegram
    text = (
        f"🚨 <b>Новая заявка с сайта!</b>\n\n"
        f"🛠 <b>Услуга:</b> {service}\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Контакт:</b> {contact}\n"
        f"💬 <b>Комментарий:</b> {comment}"
    )

    # Отправка через Telegram Bot API
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "details": response.text}), 500

if __name__ == '__main__':
    # Запуск локального сервера
    app.run(host='127.0.0.1', port=5000, debug=True)