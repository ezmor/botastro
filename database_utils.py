import sys
import logging
from datetime import datetime, timezone
from database import Lead, engine
from sqlalchemy.orm import sessionmaker
from database import DialogueHistory
from manychat_api import get_user_info

Session = sessionmaker(bind=engine)

def convert_datetime_format(iso_datetime):
    parsed_datetime = datetime.fromisoformat(iso_datetime)
    local_datetime = parsed_datetime.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return local_datetime

def upsert_lead(user_id, name=None, phone=None, birth_date=None, birth_time=None, birth_city=None, problem=None):
    session = Session()
    lead = session.query(Lead).filter_by(user_id=user_id).first()

    if lead is None:
        user_info = get_user_info(user_id)
        if user_info is None:
            print("Error: Could not retrieve user info.")
            return

        user_data = user_info['data']

        lead = Lead(
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
    if birth_time is not None:
        lead.birth_time = birth_time
    if birth_city is not None:
        lead.birth_city = birth_city
    if problem is not None:
        lead.problem = problem

    session.commit()
    session.close()



def retrieve_lead(user_id):
    session = Session()
    lead = session.query(Lead).filter(Lead.user_id == user_id).one_or_none()
    session.close()
    return lead

def get_lead_info(user_id):
    lead = retrieve_lead(user_id)
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
    sys.stderr.write("Текст, который вы хотите вывести\n")

def get_dialogue_history(user_id):
    session = Session()
    history = session.query(DialogueHistory).filter(DialogueHistory.user_id == user_id).order_by(DialogueHistory.timestamp.desc()).limit(2).all()
    session.close()
    return history[::-1]  # Вернуть сообщения в правильном порядке (от старых к новым)



