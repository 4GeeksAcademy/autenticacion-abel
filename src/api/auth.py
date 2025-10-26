import datetime
import os

import jwt

SECRET = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"


def create_token(user_id, minutes=60):
    now = datetime.datetime.utcnow()
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + datetime.timedelta(minutes=minutes),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
