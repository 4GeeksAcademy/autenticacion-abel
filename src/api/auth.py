import datetime
import os
import uuid

import jwt

SECRET = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"


def create_token(user_id, minutes=60):
    now = datetime.datetime.now(datetime.timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=minutes)).timestamp()),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except Exception:
        return None

    # check whether token jti has been revoked
    try:
        from api.models import RevokedToken

        jti = payload.get("jti")
        if jti and RevokedToken.query.filter_by(jti=jti).first():
            return None
    except Exception:
        # any DB error -> treat token as invalid
        return None

    return payload
