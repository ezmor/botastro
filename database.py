from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://botastro:3Eibf1GDPKcBfbe@64.226.126.218/botastro"

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    name = Column(String(255))
    phone = Column(String(255))
    birth_date = Column(Date)
    birth_time = Column(Time)
    birth_city = Column(String(255))

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

