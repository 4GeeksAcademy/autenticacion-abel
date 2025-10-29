import datetime
import os
import uuid

import jwt

SECRET = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"


def create_token(user_id, email=None, minutes=60):
    now = datetime.datetime.now(datetime.timezone.utc)
    jti = uuid.uuid4().hex
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=minutes)).timestamp()),
    }
    if email:
        payload["email"] = email
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except Exception:
        return None

    try:
        from api.models import RevokedToken

        jti = payload.get("jti")
        if jti and RevokedToken.query.filter_by(jti=jti).first():
            return None
    except Exception:
        return None

    return payload
