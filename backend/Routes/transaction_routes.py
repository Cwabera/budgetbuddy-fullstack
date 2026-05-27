from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, Transaction, Category

transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transactions")


@transaction_bp.get("")
@jwt_required()
def get_transactions():
    user_id = int(get_jwt_identity())

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    return [transaction.to_dict() for transaction in transactions], 200


@transaction_bp.post("")
@jwt_required()
def create_transaction():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    title = data.get("title")
    amount = data.get("amount")
    transaction_type = data.get("transaction_type")
    category_name = data.get("category")
    transaction_date = data.get("date")

    if not title or amount is None or not transaction_type:
        return {"error": "Title, amount and transaction_type are required"}, 400

    if transaction_type not in ["income", "expense"]:
        return {"error": "transaction_type must be income or expense"}, 400

    category = None

    if category_name:
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

    parsed_date = datetime.strptime(transaction_date, "%Y-%m-%d").date() if transaction_date else None

    transaction = Transaction(
        title=title,
        amount=float(amount),
        transaction_type=transaction_type,
        date=parsed_date,
        user_id=user_id,
        category_id=category.id if category else None
    )

    db.session.add(transaction)
    db.session.commit()

    return transaction.to_dict(), 201


@transaction_bp.patch("/<int:id>")
@jwt_required()
def update_transaction(id):
    user_id = int(get_jwt_identity())

    transaction = Transaction.query.get(id)

    if not transaction:
        return {"error": "Transaction not found"}, 404

    if transaction.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    data = request.get_json()

    transaction.title = data.get("title", transaction.title)
    transaction.amount = float(data.get("amount", transaction.amount))
    transaction.transaction_type = data.get("transaction_type", transaction.transaction_type)

    if "category" in data:
        category_name = data.get("category")

        if category_name:
            category = Category.query.filter_by(name=category_name).first()

            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

            transaction.category_id = category.id
        else:
            transaction.category_id = None

    if data.get("date"):
        transaction.date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()

    db.session.commit()

    return transaction.to_dict(), 200


@transaction_bp.delete("/<int:id>")
@jwt_required()
def delete_transaction(id):
    user_id = int(get_jwt_identity())

    transaction = Transaction.query.get(id)

    if not transaction:
        return {"error": "Transaction not found"}, 404

    if transaction.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(transaction)
    db.session.commit()

    return {"message": "Transaction deleted successfully"}, 200