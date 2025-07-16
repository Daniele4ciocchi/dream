from flask import Blueprint, request, jsonify, current_app
import jwt
from functools import wraps

main_bp = Blueprint("main", __name__)

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        try:
            decoded = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        return f(user_id=decoded["user_id"], *args, **kwargs)
    return wrapper

@main_bp.route("/protected", methods=["GET"])
@token_required
def protected(user_id):
    return jsonify({"message": f"Access granted for user {user_id}"})
