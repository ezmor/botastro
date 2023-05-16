from sqlalchemy import create_engine, Column, Integer, String, Date, Time, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "mysql+mysqlconnector://botastro:3Eibf1GDPKcBfbe@64.226.126.218/botastro"


# Create Base and define schema
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, unique=True)
    name = Column(String(255))
    phone = Column(String(255))
    birth_date = Column(String(255))
    birth_time = Column(String(255))
    birth_city = Column(String(255))
    problem = Column(String(255))
    page_id = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    gender = Column(String(255))
    locale = Column(String(255))
    language = Column(String(255))
    timezone = Column(String(255))
    last_input_text = Column(String(255))
    subscribed = Column(DateTime)
    last_interaction = Column(DateTime)
    last_seen = Column(DateTime)


class lead_fit_ro_mess(Base):
    __tablename__ = "lead_fit_ro_mess"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, unique=True)
    name = Column(String(255))
    phone = Column(String(255))
    birth_date = Column(String(255))
    age_w_h = Column(String(255))
    food_blood = Column(String(255))
    lose_a_term = Column(String(255))
    activity_day = Column(String(255))
    tone_message = Column(String(255)) #тональность сообщения
    answer_a = Column(String(255)) #ответ ассистента
    answer_u = Column(String(255)) #ответ пользователя
    page_id = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    gender = Column(String(255))
    locale = Column(String(255))
    language = Column(String(255))
    timezone = Column(String(255))
    last_input_text = Column(String(255))
    subscribed = Column(DateTime)
    last_interaction = Column(DateTime)
    last_seen = Column(DateTime)


class DialogueHistory(Base):
    __tablename__ = "dialogue_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    content = Column(String(4096), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Create engine and bind session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_lead(user_id, name=None):
    session = Session()
    lead = Lead(user_id=user_id, name=name)
    session.add(lead)
    session.commit()
    session.close()

def update_lead(user_id, **kwargs):
    session = Session()
    lead = session.query(Lead).filter(Lead.user_id == user_id).first()

    if lead:
        for key, value in kwargs.items():
            setattr(lead, key, value)

        session.commit()
        session.close()

def get_lead(user_id):
    session = Session()
    lead = session.query(Lead).filter(Lead.user_id == user_id).first()
    session.close()
    return lead


def store_lead_info(user_id, name, phone, birth_date, birth_time, birth_city):
    session = Session()
    lead = Lead(user_id=user_id, name=name, phone=phone, birth_date=birth_date, birth_time=birth_time, birth_city=birth_city)
    session.add(lead)
    session.commit()
    session.close()

def retrieve_lead(user_id):
    session = Session()
    lead = session.query(Lead).filter(Lead.user_id == user_id).first()
    session.close()
    return lead


def add_lead_fit_ro_mess(user_id, name=None):
    session = Session()
    lead = lead_fit_ro_mess(user_id=user_id, name=name)
    session.add(lead)
    session.commit()
    session.close()

def update_lead_fit_ro_mess(user_id, **kwargs):
    session = Session()
    lead = session.query(lead_fit_ro_mess).filter(lead_fit_ro_mess.user_id == user_id).first()

    if lead:
        for key, value in kwargs.items():
            setattr(lead, key, value)

        session.commit()
        session.close()

def get_lead_fit_ro_mess(user_id):
    session = Session()
    lead = session.query(lead_fit_ro_mess).filter(lead_fit_ro_mess.user_id == user_id).first()
    session.close()
    return lead

def store_lead_fit_ro_mess_info(user_id, name, phone, birth_date, age_w_h, food_blood, lose_a_term, activity_day):
    session = Session()
    lead = lead_fit_ro_mess(user_id=user_id, name=name, phone=phone, birth_date=birth_date, age_w_h=age_w_h, food_blood=food_blood, lose_a_term=lose_a_term, activity_day=activity_day)
    session.add(lead)
    session.commit()
    session.close()

def retrieve_lead_fit_ro_mess(user_id):
    session = Session()
    lead = session.query(lead_fit_ro_mess).filter(lead_fit_ro_mess.user_id == user_id).first()
    session.close()
    return lead

