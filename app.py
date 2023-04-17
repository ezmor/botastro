from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.DEBUG)
import json
from dialogue_script import (
    handle_welcome,
    handle_amulet_request,
    handle_phone_input,
    handle_name_input,
    handle_question,
    store_lead_info,
)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_id = data["user_id"]

    if "tag" in data:
        tag = data["tag"]["slug"]

        if tag == "welcome":
            handle_welcome(user_id)
        elif tag == "amulet_request":
            handle_amulet_request(user_id)
        elif tag == "phone_input":
            phone = data["custom_field"]["value"]
            handle_phone_input(user_id, phone)
        elif tag == "name_input":
            name = data["custom_field"]["value"]
            # Здесь мы предполагаем, что вы сохраняете номер телефона клиента в кастомное поле ManyChat.
            # Вы должны заменить "phone_custom_field_id" на ID кастомного поля, которое содержит номер телефона.
            phone = data["subscriber"]["custom_fields"]["phone_custom_field_id"]
            handle_name_input(user_id, name, phone)
            
            # Допустим, пользователь предоставил всю информацию о дате и времени рождения и городе рождения.
            # Вы должны заменить "birth_date_custom_field_id", "birth_time_custom_field_id" и "birth_city_custom_field_id"
            # на соответствующие ID кастомных полей, которые содержат эту информацию.
            birth_date = data["subscriber"]["custom_fields"]["birth_date_custom_field_id"]
            birth_time = data["subscriber"]["custom_fields"]["birth_time_custom_field_id"]
            birth_city = data["subscriber"]["custom_fields"]["birth_city_custom_field_id"]
            
            # Сохраняем информацию о лиде в базе данных
            store_lead_info(user_id, name, phone, birth_date, birth_time, birth_city)

    else:
        message = data["message"]
        response_text = handle_question(user_id, message)
        response = {
            "version": "v2",
            "content": {
                "messages": [
                    {
                        "type": "text",
                        "text": response_text
                    }
                ],
                "actions": [],
                "quick_replies": []
            }
        }
        return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
