import sys
import logging
from datetime import datetime, timezone
from database import lead_fit_ro_mess, engine
from sqlalchemy.orm import sessionmaker
from database import DialogueHistory
from manychat_api import get_user_info

Session = sessionmaker(bind=engine)

def convert_datetime_format(iso_datetime):
    parsed_datetime = datetime.fromisoformat(iso_datetime)
    local_datetime = parsed_datetime.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return local_datetime

def upsert_lead(user_id, name=None, phone=None, birth_date=None, age_w_h=None, food_blood=None, lose_a_term=None, activity_day=None, answer_a=None, answer_u=None, tone_message=None):
    session = Session()
    lead = session.query(lead_fit_ro_mess).filter_by(user_id=user_id).first()

    if lead is None:
        user_info = get_user_info(user_id)
        if user_info is None:
            print("Error: Could not retrieve user info.")
            return

        user_data = user_info['data']

        lead = lead_fit_ro_mess(
            user_id=user_id,
            page_id=user_data.get('page_id'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            gender=user_data.get('gender'),
            locale=user_data.get('locale'),
            language=user_data.get('language'),
            timezone=user_data.get('timezone'),
            last_input_text=user_data.get('last_input_text'),
            subscribed=convert_datetime_format(user_data.get('subscribed')) if user_data.get('subscribed') else None,
            last_interaction=convert_datetime_format(user_data.get('last_interaction')) if user_data.get('last_interaction') else None,
            last_seen=convert_datetime_format(user_data.get('last_seen')) if user_data.get('last_seen') else None
        )

        session.add(lead)

    if name is not None:
        lead.name = name
    if phone is not None:
        lead.phone = phone
    if birth_date is not None:
        lead.birth_date = birth_date
    if age_w_h is not None:
        lead.age_w_h = age_w_h
    if food_blood is not None:
        lead.food_blood = food_blood
    if lose_a_term is not None:
        lead.lose_a_term = lose_a_term
    if activity_day is not None:
        lead.activity_day = activity_day
    if answer_a is not None:
        lead.answer_a = answer_a
    if answer_u is not None:
        lead.answer_u = answer_u
    if tone_message is not None:
        lead.tone_message = tone_message


    session.commit()
    session.close()

def retrieve_lead_fit_ro_mess(user_id):
    session = Session()
    lead = session.query(lead_fit_ro_mess).filter(lead_fit_ro_mess.user_id == user_id).one_or_none()
    session.close()
    return lead

def get_lead_fit_ro_mess_info(user_id):
    lead = retrieve_lead_fit_ro_mess(user_id)
    if lead is not None:
        lead_info = {}
        for column in lead.__table__.columns:
            lead_info[column.name] = getattr(lead, column.name)
        return lead_info
    else:
        return None

def add_message(user_id, role, content):
    logging.debug(f"Adding message: user_id={user_id}, role={role}, content={content}")
    session = Session()
    message = DialogueHistory(user_id=user_id, role=role, content=content)
    session.add(message)
    session.commit()
    session.close()

def get_dialogue_history(user_id):
    session = Session()
    history = session.query(DialogueHistory).filter(DialogueHistory.user_id == user_id).order_by(DialogueHistory.timestamp.desc()).limit(2).all()
    session.close()
    return history[::-1]  # Вернуть сообщения в правильном порядке (от старых к новым)
