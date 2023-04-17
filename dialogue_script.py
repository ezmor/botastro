from manychat_api import send_message, get_user_info
from gpt_api import generate_response
from crm_integration import send_order_to_crm
from config import WELCOME_MESSAGE, AMULET_PROMPT, AMULET_MORE_INFO, PHONE_PROMPT, NAME_PROMPT, THANK_YOU_MESSAGE
from statistics import increment_conversations, increment_sales
from utils import clean_phone_number
from database import Lead, session
import requests


API_TOKEN = '106153512442485:3fada7a2f914d2760f8afb2c3effb0fb'


# Обработка приветствия
def handle_welcome(user_id):
    send_message(user_id, WELCOME_MESSAGE)
    increment_conversations()

# Обработка запроса об амулете
def handle_amulet_request(user_id):
    send_message(user_id, AMULET_MORE_INFO)
    send_message(user_id, PHONE_PROMPT)

# Обработка получения номера телефона
def handle_phone_input(user_id, phone):
    cleaned_phone = clean_phone_number(phone)
    send_order_to_crm(None, cleaned_phone)  # временно сохраняем телефон в CRM без имени
    send_message(user_id, NAME_PROMPT)

# Обработка получения имени клиента
def handle_name_input(user_id, name, phone):
    send_order_to_crm(name, phone)  # обновляем запись в CRM с полными данными клиента
    send_message(user_id, THANK_YOU_MESSAGE)
    increment_sales()

# Обработка вопросов от клиента
def handle_question(user_id, question):
    response = generate_response(question)
    send_message(user_id, response)

# Функции связанные с астрологическим скриптом
def store_lead_info(user_id, name, phone, birth_date, birth_time, birth_city):
    lead = Lead(user_id=user_id, name=name, phone=phone, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city)
    session.add(lead)
    session.commit()


def send_message(user_id, message):
    url = f"https://api.manychat.com/fb/sending/sendContent?subscriber_id={user_id}&api_token={API_TOKEN}"
    data = {
        "message": {
            "text": message
        }
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    return message
