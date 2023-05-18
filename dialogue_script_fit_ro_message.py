# -*- coding: utf-8 -*-
import requests
import re
import phonenumbers
import logging
import numpy
import time
import simplejson as json
from manychat_api import set_custom_field, get_user_info, add_tag_by_name, remove_tag_by_name
from gpt_api import generate_response_with_variables, generate_response_with_variables_turbo, generate_response_with_variables_gpt4
from crm_integration import send_order_to_crm
from config_fit_ro_mess import (
    PROFILE_FIT,
    OFFER,
    ANSWER_QUESTION_ANALYSIS,
    ROLE_ANSWER_QUESTION_ANALYSIS,
    ROLE_ANSWER_INTEREST,
    ANSWER_INTEREST,
    ROLE_ANSWER_DOUBTS,
    ANSWER_DOUBTS,
    ROLE_ANSWER_NEGATIVE,
    ANSWER_NEGATIVE,
    ROLE_ANSWER_OTHER,
    ANSWER_OTHER,
    ROLE_PROFILE_FIT,
    ROLE_OFFER
)
from statistics import increment_conversations, increment_sales
from utils import clean_phone_number
from database import Lead, session, update_lead_fit_ro_mess, retrieve_lead_fit_ro_mess, add_lead_fit_ro_mess, DialogueHistory, engine
from sqlalchemy.orm import sessionmaker
from database_utils_fit_ro_mess import add_message, upsert_lead, get_lead_fit_ro_mess_info, get_dialogue_history

Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.DEBUG)

API_TOKEN = '106153512442485:3fada7a2f914d2760f8afb2c3effb0fb'

def fit_ro_message(user_id, message, tag):
    response = None
    if tag == 'birth_date':
        response = handle_birth_date(user_id, message)
    elif tag == 'age_w_h':
        response = handle_age_w_h(user_id, message)
        logging.info(f"Message for age_w_h: {message}")
    elif tag == 'food_blood':
        response = handle_food_blood(user_id, message)
    elif tag == 'lose_a_term':
        response = handle_lose_a_term(user_id, message)
    elif tag == 'activity_day':
        response = handle_activity_day(user_id, message)
    elif tag == 'profile_fit':
        lead_fit_ro_mess = get_lead_fit_ro_mess_info(user_id)
        response = handle_profile_fit(user_id, lead_fit_ro_mess['age_w_h'], lead_fit_ro_mess['food_blood'], lead_fit_ro_mess['lose_a_term'], lead_fit_ro_mess['activity_day'], lead_fit_ro_mess['first_name'], lead_fit_ro_mess['gender'])
    elif tag == 'offer':
        lead_fit_ro_mess = get_lead_fit_ro_mess_info(user_id)
        response = handle_offer(user_id, lead_fit_ro_mess['age_w_h'], lead_fit_ro_mess['food_blood'], lead_fit_ro_mess['lose_a_term'], lead_fit_ro_mess['activity_day'], lead_fit_ro_mess['first_name'], lead_fit_ro_mess['gender'])
    elif tag == 'answer_question': #Сюда шлем запрос с сообщением пользователя
        lead_fit_ro_mess = get_lead_fit_ro_mess_info(user_id)
        response = handle_answer_question(user_id, message, lead_fit_ro_mess['age_w_h'], lead_fit_ro_mess['food_blood'], lead_fit_ro_mess['lose_a_term'], lead_fit_ro_mess['activity_day'], lead_fit_ro_mess['first_name'], lead_fit_ro_mess['gender'], lead_fit_ro_mess['answer_a'])
    else:
        response = handle_unknown_state(user_id)

    return response

def handle_birth_date(user_id, birth_date):
    upsert_lead(user_id, birth_date=birth_date)

def handle_age_w_h(user_id, age_w_h):
    logging.info(f"Received data: {age_w_h}")
    upsert_lead(user_id, age_w_h=age_w_h)
    add_tag_by_name (user_id, tag_name="age_w_h")

def handle_food_blood(user_id, food_blood):
    upsert_lead(user_id, food_blood=food_blood)
    remove_tag_by_name (user_id, tag_name="age_w_h")
    add_tag_by_name (user_id, tag_name="food_blood")

def handle_lose_a_term(user_id, lose_a_term):
    upsert_lead(user_id, lose_a_term=lose_a_term)
    remove_tag_by_name (user_id, tag_name="food_blood")
    add_tag_by_name (user_id, tag_name="lose_a_term")

def handle_activity_day(user_id, activity_day):
    upsert_lead(user_id, activity_day=activity_day)
    remove_tag_by_name (user_id, tag_name="lose_a_term")
    add_tag_by_name (user_id, tag_name="activity_day")

def handle_profile_fit(user_id, age_w_h, food_blood, lose_a_term, activity_day, first_name, gender):
    response = generate_response_with_variables_gpt4(PROFILE_FIT, ROLE_PROFILE_FIT, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender)
    set_custom_field(user_id, "9313462", f'"{response}"')
    logging.error(f"Response: {response}")
    return response


def handle_offer(user_id, age_w_h, food_blood, lose_a_term, activity_day, first_name, gender):
    response = generate_response_with_variables_gpt4(OFFER, ROLE_OFFER, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender)
    set_custom_field(user_id, "9313459", f'"{response}"')
    upsert_lead(user_id, answer_a=response)
    return response

def handle_answer_question(user_id, message, age_w_h, food_blood, lose_a_term, activity_day, first_name, gender, answer_a):
    upsert_lead(user_id, answer_u=message)
    response_analys = generate_response_with_variables_gpt4(ANSWER_QUESTION_ANALYSIS, ROLE_ANSWER_QUESTION_ANALYSIS, max_tokens=1000, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender, answer_a=answer_a, answer_u=message)
    upsert_lead(user_id, tone_message=response_analys)
    if 'заинтересованность' in response_analys:
        response = generate_response_with_variables_gpt4(ANSWER_INTEREST, ROLE_ANSWER_INTEREST, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender, answer_a=answer_a, answer_u=message)
        set_custom_field(user_id, "9313460", f'"{response}"')
        return response
        pass
    elif 'сомнения' in response_analys:
        response = generate_response_with_variables_gpt4(ANSWER_DOUBTS, ROLE_ANSWER_DOUBTS, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender, answer_a=answer_a, answer_u=message)
        set_custom_field(user_id, "9313460", f'"{response}"')
        return response
        pass
    elif 'негативный' in response_analys:
        response = generate_response_with_variables_gpt4(ANSWER_NEGATIVE, ROLE_ANSWER_NEGATIVE, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender, answer_a=answer_a, answer_u=message)
        set_custom_field(user_id, "9313460", f'"{response}"')
        return response
        pass
    elif 'другие вопросы' in response_analys:
        response = generate_response_with_variables_gpt4(ANSWER_OTHER, ROLE_ANSWER_OTHER, max_tokens=1500, temperature=0.9, top_p=0.7, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day, first_name=first_name, gender=gender, answer_a=answer_a, answer_u=message)
        set_custom_field(user_id, "9313460", f'"{response}"')
        return response
        pass
    remove_tag_by_name (user_id, tag_name="activity_day")
    add_tag_by_name (user_id, tag_name="handle_answer_question")


def is_valid_phone_number(phone, default_region="UA"):
    try:
        parsed_number = phonenumbers.parse(phone, default_region)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False

def handle_unknown_state(user_id):
    response = "Извините, возникла непредвиденная ситуация. Пожалуйста, повторите ваш запрос."
    set_custom_field(user_id, response)
    return response


