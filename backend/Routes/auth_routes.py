from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models import db, User

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "Username, email and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return {
        "message": "User registered successfully",
        "user": user.to_dict(),
        "token": token
    }, 201


@auth_bp.post("/login")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "user": user.to_dict(),
        "token": token
    }, 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return user.to_dict(), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    return {"message": "Logout successful"}, 200