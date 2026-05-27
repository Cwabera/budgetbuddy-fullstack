import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { user } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {
    async function loadData() {
      const transactionData = await apiRequest("/transactions");
      const budgetData = await apiRequest("/budgets");

      setTransactions(transactionData);
      setBudgets(budgetData);
    }

    loadData();
  }, []);

  const income = transactions
    .filter((item) => item.transaction_type === "income")
    .reduce((sum, item) => sum + item.amount, 0);

  const expenses = transactions
    .filter((item) => item.transaction_type === "expense")
    .reduce((sum, item) => sum + item.amount, 0);

  const balance = income - expenses;

  return (
    <main className="page">
      <h2>Welcome, {user?.username}</h2>

      <div className="cards">
        <div className="card">
          <h3>Total Income</h3>
          <p>KES {income.toLocaleString()}</p>
        </div>

        <div className="card">
          <h3>Total Expenses</h3>
          <p>KES {expenses.toLocaleString()}</p>
        </div>

        <div className="card">
          <h3>Balance</h3>
          <p>KES {balance.toLocaleString()}</p>
        </div>

        <div className="card">
          <h3>Budgets</h3>
          <p>{budgets.length}</p>
        </div>
      </div>
    </main>
  );
}

export default Dashboard;