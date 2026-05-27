from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Budget, Category

budget_bp = Blueprint("budget_bp", __name__, url_prefix="/budgets")


@budget_bp.get("")
@jwt_required()
def get_budgets():
    user_id = int(get_jwt_identity())

    budgets = Budget.query.filter_by(user_id=user_id).all()

    return [budget.to_dict() for budget in budgets], 200


@budget_bp.post("")
@jwt_required()
def create_budget():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    name = data.get("name")
    limit_amount = data.get("limit_amount")
    category_names = data.get("categories", [])

    if not name or limit_amount is None:
        return {"error": "Name and limit_amount are required"}, 400

    budget = Budget(
        name=name,
        limit_amount=float(limit_amount),
        user_id=user_id
    )

    for category_name in category_names:
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            category = Category(name=category_name)
            db.session.add(category)

        budget.categories.append(category)

    db.session.add(budget)
    db.session.commit()

    return budget.to_dict(), 201


@budget_bp.patch("/<int:id>")
@jwt_required()
def update_budget(id):
    user_id = int(get_jwt_identity())

    budget = Budget.query.get(id)

    if not budget:
        return {"error": "Budget not found"}, 404

    if budget.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    data = request.get_json()

    budget.name = data.get("name", budget.name)
    budget.limit_amount = float(data.get("limit_amount", budget.limit_amount))

    if "categories" in data:
        budget.categories.clear()

        for category_name in data.get("categories", []):
            category = Category.query.filter_by(name=category_name).first()

            if not category:
                category = Category(name=category_name)
                db.session.add(category)

            budget.categories.append(category)

    db.session.commit()

    return budget.to_dict(), 200


@budget_bp.delete("/<int:id>")
@jwt_required()
def delete_budget(id):
    user_id = int(get_jwt_identity())

    budget = Budget.query.get(id)

    if not budget:
        return {"error": "Budget not found"}, 404

    if budget.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(budget)
    db.session.commit()

    return {"message": "Budget deleted successfully"}, 200