from flask import request, jsonify, Blueprint
from api.models import db, User
from api.utils import APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from api.auth import create_token, verify_token

api = Blueprint('api', __name__)

CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        raise APIException('email and password required', status_code=400)
    existing = User.query.filter_by(email=email).first()
    if existing:
        raise APIException('user exists', status_code=400)
    pw_hash = generate_password_hash(password)
    user = User(email=email, password=pw_hash, is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created'}), 200


@api.route('/token', methods=['POST'])
def token():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'email and password required'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'invalid credentials'}), 401
    token = create_token(user.id)
    return jsonify({'token': token}), 200


@api.route('/private', methods=['GET'])
def private():
    auth = request.headers.get('Authorization', '')
    token = None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        token = parts[1]
    if not token:
        token = request.args.get('token')
    if not token:
        return jsonify({'message': 'missing token'}), 401
    payload = verify_token(token)
    if not payload:
        return jsonify({'message': 'invalid token'}), 401
    user_id = payload.get('sub')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'user not found'}), 401
    return jsonify({'message': 'access granted', 'user': user.serialize()}), 200
