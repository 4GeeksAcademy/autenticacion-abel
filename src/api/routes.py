from flask import Blueprint, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

from api.auth import create_token, verify_token
from api.models import User, db
from api.utils import APIException

api = Blueprint("api", __name__)

CORS(api)


@api.route("/hello", methods=["POST", "GET"])
def handle_hello():
    response_body = {
        "message": "Hello from backend — open the network tab to see requests"
    }
    return jsonify(response_body), 200


@api.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise APIException("email and password required", status_code=400)
    existing = User.query.filter_by(email=email).first()
    if existing:
        raise APIException("user exists", status_code=400)
    pw_hash = generate_password_hash(password)
    user = User(email=email, password=pw_hash, is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user created"}), 200


@api.route("/token", methods=["POST"])
def token():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "invalid credentials"}), 401
    token = create_token(user.id, email=user.email)
    return jsonify({"token": token}), 200


@api.route("/private", methods=["GET"])
def private():
    auth = request.headers.get("Authorization", "")
    token = None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    if not token:
        token = request.args.get("token")
    if not token:
        return jsonify({"message": "missing token"}), 401
    payload = verify_token(token)
    if not payload:
        return jsonify({"message": "invalid token"}), 401

    # token ok -> lookup user by id
    user_id = payload.get("sub")
    # use Session.get for SQLAlchemy 1.x+ compatibility
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "user not found"}), 401
    return jsonify({"message": "access granted", "user": user.serialize()}), 200


@api.route("/logout", methods=["POST"])
def logout():
    auth = request.headers.get("Authorization", "")
    token = None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    if not token:
        token = request.get_json(silent=True) or {}
        token = token.get("token") if isinstance(token, dict) else None
    if not token:
        token = request.args.get("token")
    if not token:
        return jsonify({"message": "missing token"}), 400

    try:
        import jwt

        from api.auth import ALGORITHM, SECRET
        from api.models import RevokedToken

        payload = jwt.decode(
            token, SECRET, algorithms=[ALGORITHM], options={"verify_exp": False}
        )
        jti = payload.get("jti")
        if not jti:
            return jsonify({"message": "invalid token"}), 400
        if not RevokedToken.query.filter_by(jti=jti).first():
            rt = RevokedToken(jti=jti)
            db.session.add(rt)
            db.session.commit()
        return jsonify({"message": "token revoked"}), 200
    except Exception:
        return jsonify({"message": "invalid token"}), 400
