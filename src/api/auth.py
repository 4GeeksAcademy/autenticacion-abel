import datetime
import os

import jwt

SECRET = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"


def create_token(user_id, minutes=60):
    # use timezone-aware UTC datetimes to avoid deprecation warnings
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": str(user_id),
        # issued-at and expiration must be numeric timestamps for JWTs
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=minutes)).timestamp()),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
