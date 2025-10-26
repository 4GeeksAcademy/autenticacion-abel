import datetime
import os
import uuid

import jwt

SECRET = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"


def create_token(user_id, email=None, minutes=60):
    # use timezone-aware UTC datetimes to avoid deprecation warnings
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": str(user_id),
        # issued-at and expiration must be numeric timestamps for JWTs
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=minutes)).timestamp()),
        # unique id for the token so we can blacklist it
        "jti": uuid.uuid4().hex,
    }
    if email:
        payload["email"] = email
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        # check if token is revoked
        try:
            from api.models import RevokedToken

            jti = payload.get("jti")
            if jti:
                revoked = RevokedToken.query.filter_by(jti=jti).first()
                if revoked:
                    return None
        except Exception:
            # If models or DB aren't available (early import), skip blacklist check.
            pass
        return payload
    except Exception:
        return None
