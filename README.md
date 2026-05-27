# 💰 BudgetBuddy Full Stack

## 📌 Project Description

BudgetBuddy Full Stack is a personal finance management web application built using React and Flask. The application allows users to register, log in securely, manage budgets, track income and expenses, and organize spending into categories.

This project is an evolution of the original BudgetBuddy CLI application into a modern full-stack web application with authentication, database relationships, protected routes, and a responsive user interface.

---

# 🚀 Features

## Authentication
- User Registration
- User Login
- JWT Authentication
- Protected Routes
- Persistent User Sessions

## Budget Management
- Create Budgets
- View Budgets
- Update Budgets
- Delete Budgets

## Transaction Management
- Add Transactions
- Track Income & Expenses
- Categorize Transactions
- Delete Transactions
- View Financial Summary

## Dashboard
- Total Income
- Total Expenses
- Remaining Balance
- Budget Overview

---

# 🛠️ Technologies Used

## Frontend
- React
- React Router DOM
- Context API
- CSS

## Backend
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask Migrate
- Flask CORS

## Database
- SQLite

---

# 🧠 Concepts Demonstrated

- Full Stack Development
- REST API Design
- JWT Authentication
- CRUD Operations
- React Hooks
- React Router
- Protected Routes
- One-to-Many Relationships
- Many-to-Many Relationships
- Database Migrations
- State Management
- Responsive Design

---

# 🗂️ Database Relationships

## One-to-Many
- One User can have many Transactions
- One User can have many Budgets

## Many-to-Many
- Many Budgets can contain many Categories
- Many Categories can belong to many Budgets

---

# 📁 Project Structure

```txt
budgetbuddy-fullstack/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── routes/
│   └── migrations/
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── context/
    │   ├── pages/
    │   ├── services/
    │   ├── App.jsx
    │   └── main.jsx
    │
    └── package.json
