from app import app
from models import db, User, Category, Transaction, Budget

with app.app_context():
    Transaction.query.delete()
    Budget.query.delete()
    Category.query.delete()
    User.query.delete()

    user = User(username="Charles", email="charles@example.com")
    user.set_password("password123")

    db.session.add(user)
    db.session.commit()

    food = Category(name="Food")
    transport = Category(name="Transport")
    rent = Category(name="Rent")
    salary = Category(name="Salary")

    db.session.add_all([food, transport, rent, salary])
    db.session.commit()

    transaction1 = Transaction(
        title="Monthly Salary",
        amount=80000,
        transaction_type="income",
        user_id=user.id,
        category_id=salary.id
    )

    transaction2 = Transaction(
        title="Groceries",
        amount=3500,
        transaction_type="expense",
        user_id=user.id,
        category_id=food.id
    )

    transaction3 = Transaction(
        title="Bus Fare",
        amount=300,
        transaction_type="expense",
        user_id=user.id,
        category_id=transport.id
    )

    budget1 = Budget(
        name="Monthly Essentials",
        limit_amount=30000,
        user_id=user.id
    )

    budget1.categories.append(food)
    budget1.categories.append(transport)
    budget1.categories.append(rent)

    db.session.add_all([transaction1, transaction2, transaction3, budget1])
    db.session.commit()

    print("BudgetBuddy database seeded successfully!")
    