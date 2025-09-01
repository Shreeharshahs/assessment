import uuid
from datetime import datetime, timedelta
SESSION_STORE = {}

SESSION_DURATION_MINUTES = 1

def create_session(teacher_id):
    token = uuid.uuid4().hex
    expiry = datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES)
    SESSION_STORE[token] = (teacher_id, expiry)
    return token

def get_teacher_id_from_token(token):
    session = SESSION_STORE.get(token)
    if not session:
        return None
    teacher_id, expiry = session
    if datetime.utcnow() > expiry:
        del SESSION_STORE[token]
        return None
    return teacher_id

def destroy_session(token):
    if token in SESSION_STORE:
        del SESSION_STORE[token]


