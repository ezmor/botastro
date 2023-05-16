# -*- coding: utf-8 -*-
import requests
import re
import phonenumbers
import logging
import numpy
import simplejson as json
from manychat_api import send_whatsapp, get_user_info
from gpt_api import generate_response_with_variables, generate_response_with_variables_turbo, generate_response_with_variables_gpt4
from crm_integration import send_order_to_crm
from config import (
    GREETING,
    FREE_HOROSCOPE_OFFER,
    COLLECT_birth_date,
    COLLECT_BIRTH_TIME,
    COLLECT_BIRTH_CITY,
    ASK_PROBLEM,
    PROBLEM_ANSWER,
    ANALYZE_HOROSCOPE,
    AMULET_PRESENTATION,
    REQUEST_CONTACT_INFO,
    FINAL_MESSAGE,
    ROLE_AMELET,
    ROLE_AMULET_PRESENTATION
)
from statistics import increment_conversations, increment_sales
from utils import clean_phone_number
from database import Lead, session, update_lead, retrieve_lead, add_lead, DialogueHistory, engine
from sqlalchemy.orm import sessionmaker
from database_utils import add_message, upsert_lead, get_lead_info, get_dialogue_history

Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.DEBUG)

API_TOKEN = '106153512442485:3fada7a2f914d2760f8afb2c3effb0fb'

def astro_whatsapp(user_id, message, tag):
    response = None
    if tag == 'welcome':
        response = handle_greeting(user_id)
    elif tag == 'birth_date':
        response = handle_birth_date(user_id)
    elif tag == 'handle_birth_time':
        response = handle_birth_time(user_id, message)
    elif tag == 'handle_birth_city':
        response = handle_birth_city(user_id, message)
    elif tag == 'problem':
        response = handle_problem(user_id, message)
    elif tag == 'analyze_horoscope':
        lead_info = get_lead_info(user_id)
        response = handle_analyze_horoscope(user_id, lead_info['birth_date'], lead_info['birth_time'], lead_info['birth_city'], message)
    elif tag == 'problem_horoscope':
        lead_info = get_lead_info(user_id)
        response = handle_problem_answer(user_id, lead_info['birth_date'], lead_info['birth_time'], lead_info['birth_city'], message)
    elif tag == 'amulet_present':
        lead_info = get_lead_info(user_id)
        response = handle_amulet_presentation(user_id, lead_info['birth_date'], lead_info['birth_time'], lead_info['birth_city'], message)
    elif tag == 'contact_info':
        response = handle_contact_info(user_id, message)
    elif tag == 'final_message':
        response = handle_final_message(user_id, message)
    elif tag == 'final_message_2':
        response = handle_final_message_2(user_id, message)
    else:
        response = handle_unknown_state(user_id)

    return response




def handle_greeting(user_id):
    upsert_lead(user_id)
    #response_greeting = generate_response_with_variables_gpt4(GREETING)
    #response_offer = generate_response_with_variables_gpt4(FREE_HOROSCOPE_OFFER)
    send_whatsapp(user_id, GREETING, "handle_greeting")
    send_whatsapp(user_id, FREE_HOROSCOPE_OFFER, "handle_greeting")
    return GREETING + " " + FREE_HOROSCOPE_OFFER


def handle_birth_date(user_id):
    send_whatsapp(user_id, COLLECT_birth_date, "handle_birth_date", "handle_greeting")
    return COLLECT_birth_date

def handle_birth_time(user_id, birth_date):
    upsert_lead(user_id, birth_date=birth_date)
    send_whatsapp(user_id, COLLECT_BIRTH_TIME, "handle_birth_time", "handle_birth_date")
    return COLLECT_BIRTH_TIME

def handle_birth_city(user_id, birth_time):
    upsert_lead(user_id, birth_time=birth_time)
    send_whatsapp(user_id, COLLECT_BIRTH_CITY, "handle_birth_city", "handle_birth_time")
    return COLLECT_BIRTH_CITY

def handle_problem(user_id, birth_city):
    upsert_lead(user_id, birth_city=birth_city)
    send_whatsapp(user_id, ASK_PROBLEM, "handle_problem", "handle_birth_city")
    return ASK_PROBLEM

def handle_analyze_horoscope(user_id, birth_date, birth_time, birth_city, problem):
    upsert_lead(user_id, problem=problem)
    lead_info = get_lead_info(user_id)
    first_name = lead_info.get('first_name', '') if lead_info else ''
    gender = lead_info.get('gender', '') if lead_info else ''

    response = generate_response_with_variables_gpt4(ANALYZE_HOROSCOPE, ROLE_AMELET, max_tokens=1800, temperature=0.9, top_p=0.7, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city, problem=problem, first_name=first_name, gender=gender)
    send_whatsapp(user_id, response, "handle_analyze_horoscope", "handle_problem")
    return response


def handle_problem_answer(user_id, birth_date, birth_time, birth_city, problem):
    lead_info = get_lead_info(user_id)
    if lead_info is None:
        # Здесь вы можете добавить код обработки ошибки, если информация о пользователе недоступна
        return "Извините, не удалось обработать ваш запрос."

    first_name = lead_info.get('first_name', '') if lead_info else ''
    gender = lead_info.get('gender', '') if lead_info else ''
    
    response = generate_response_with_variables_gpt4(PROBLEM_ANSWER, ROLE_AMELET, max_tokens=1800, temperature=0.9, top_p=0.7, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city, problem=problem, first_name=first_name, gender=gender)
    send_whatsapp(user_id, response, "handle_problem_answer", "handle_analyze_horoscope")
    return response


def handle_amulet_presentation(user_id, birth_date, birth_time, birth_city, problem):
    lead_info = get_lead_info(user_id)
    first_name = lead_info.get('first_name', '') if lead_info else ''
    gender = lead_info.get('gender', '') if lead_info else ''

    response = generate_response_with_variables_gpt4(AMULET_PRESENTATION, ROLE_AMULET_PRESENTATION, max_tokens=2000, temperature=0.95, top_p=0.7, presence_penalty=0, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city, problem=problem, first_name=first_name, gender=gender)
    send_whatsapp(user_id, response, "handle_amulet_presentation", "handle_problem_answer")
    return response


def handle_contact_info(user_id, message):
    response = generate_response_with_variables_gpt4(REQUEST_CONTACT_INFO, max_tokens=500, temperature=0.75, top_p=0.7, message=message)
    send_whatsapp(user_id, response, "handle_contact_info", "handle_amulet_presentation")
    return response


def handle_final_message(user_id, phone):
    logging.debug(f"Entering handle_final_message: user_id={user_id}, phone={phone}")

    if is_valid_phone_number(phone):
        upsert_lead(user_id, phone=phone)
        response = generate_response_with_variables_gpt4(FINAL_MESSAGE)
        send_whatsapp(user_id, response, "handle_final_message", "handle_contact_info")
        logging.debug(f"Phone number valid: {phone}. Sent final message.")
    else:
        history = get_dialogue_history(user_id)
        last_3_messages = history[-3:]
        last_3_messages_content = [msg.content for msg in last_3_messages]
        last_3_messages_str = "\n".join(last_3_messages_content)
        
        lead_info = get_lead_info(user_id)
        first_name = lead_info.get('first_name', '') if lead_info else ''
        gender = lead_info.get('gender', '') if lead_info else ''
        problem = lead_info.get('problem', '') if lead_info else ''
        incorrect_number_message = f"\nassistant: Пользователь {first_name}({gender}) ввел неправильный номер телефона и ответил: {phone}. Уговори его написать корректный номер телефона для покупки амулета. Ты можешь делать акцент не его проблеме: {problem}, чтобы увеличить заинтересованность в амулете с заговором который ты специально для него изготовишь.\n AI:"
        last_3_messages_str += "\n" + incorrect_number_message

        response = generate_response_with_variables_gpt4(last_3_messages_str, ROLE_AMULET_PRESENTATION, max_tokens=1250, temperature=0.9, top_p=0.5)
        send_whatsapp(user_id, response.encode('utf-8'), "handle_final_message_2", "handle_contact_info")

        logging.debug(f"Phone number invalid: {phone}. Sent message to correct. {response}")



def handle_final_message_2(user_id, phone):
    logging.debug(f"Entering handle_final_message_2: user_id={user_id}, phone={phone}")
    if is_valid_phone_number(phone):
        upsert_lead(user_id, phone=phone)
        response = generate_response_with_variables_gpt4(FINAL_MESSAGE)
        send_whatsapp(user_id, response, "handle_final_message", "handle_final_message_2")
        print(f"User {user_id} provided valid phone number: {phone}, response: {response}")
    else:
        print(f"User {user_id} provided invalid phone number: {phone}")

        history = get_dialogue_history(user_id)
        last_2_messages = history[-2:]
        last_2_messages_content = [msg.content for msg in last_2_messages]
        last_2_messages_str = "\n".join(last_2_messages_content)
        
        lead_info = get_lead_info(user_id)
        first_name = lead_info.get('first_name', '') if lead_info else ''
        gender = lead_info.get('gender', '') if lead_info else ''
        problem = lead_info.get('problem', '') if lead_info else ''
        incorrect_number_message = f"\nassistant: Пользователь {first_name}({gender}) ответил: {phone}. Уговори его написать корректный номер телефона для покупки амулета. Гарантируй ему избавиться от его проблем: {problem}, с помощью амулета с заговором который ты специально для него изготовишь.\n AI:"
        last_2_messages_str += "\n" + incorrect_number_message

        response = generate_response_with_variables_gpt4(prompt_template=last_2_messages_str, system_role=ROLE_AMULET_PRESENTATION, max_tokens=2000, temperature=0.9, top_p=0.4)
        send_whatsapp(user_id, response.encode('utf-8'))
        print(f"User {user_id} provided invalid phone number: {phone}. Sent generated response.{response.encode('utf-8')}")



def is_valid_phone_number(phone, default_region="UA"):
    try:
        parsed_number = phonenumbers.parse(phone, default_region)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False


def handle_unknown_state(user_id):
    response = "Извините, возникла непредвиденная ситуация. Пожалуйста, повторите ваш запрос."
    send_whatsapp(user_id, response)
    return response





# Функции связанные с астрологическим скриптом
def store_lead_info(user_id, name, phone, birth_date, birth_time, birth_city):
    update_lead(user_id, name=name, phone=phone, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city)



