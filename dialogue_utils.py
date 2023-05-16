# database_utils.py

from sqlalchemy.orm import sessionmaker
from database import DialogueHistory, engine

Session = sessionmaker(bind=engine)

def add_message(user_id, role, content):
    session = Session()
    message = DialogueHistory(user_id=user_id, role=role, content=content)
    session.add(message)
    session.commit()
    session.close()

def get_dialogue_history(user_id):
    session = Session()
    history = session.query(DialogueHistory).filter(DialogueHistory.user_id == user_id).order_by(DialogueHistory.timestamp.asc()).all()
    session.close()
    return history
