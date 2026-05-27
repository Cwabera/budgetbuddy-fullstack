from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from models import db, Category

category_bp = Blueprint("category_bp", __name__, url_prefix="/categories")


@category_bp.get("")
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return [category.to_dict() for category in categories], 200


@category_bp.post("")
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return {"error": "Category name is required"}, 400

    existing = Category.query.filter_by(name=name).first()

    if existing:
        return existing.to_dict(), 200

    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    return category.to_dict(), 201