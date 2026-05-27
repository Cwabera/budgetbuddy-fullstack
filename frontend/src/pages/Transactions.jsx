import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function Transactions() {
  const [transactions, setTransactions] = useState([]);

  const [formData, setFormData] = useState({
    title: "",
    amount: "",
    transaction_type: "expense",
    category: "",
    date: "",
  });

  async function loadTransactions() {
    const data = await apiRequest("/transactions");
    setTransactions(data);
  }

  useEffect(() => {
    loadTransactions();
  }, []);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    await apiRequest("/transactions", {
      method: "POST",
      body: JSON.stringify(formData),
    });

    setFormData({
      title: "",
      amount: "",
      transaction_type: "expense",
      category: "",
      date: "",
    });

    loadTransactions();
  }

  async function handleDelete(id) {
    await apiRequest(`/transactions/${id}`, {
      method: "DELETE",
    });

    loadTransactions();
  }

  return (
    <main className="page">
      <h2>Transactions</h2>

      <form onSubmit={handleSubmit} className="form grid-form">
        <input
          name="title"
          placeholder="Title"
          value={formData.title}
          onChange={handleChange}
        />

        <input
          name="amount"
          type="number"
          placeholder="Amount"
          value={formData.amount}
          onChange={handleChange}
        />

        <select
          name="transaction_type"
          value={formData.transaction_type}
          onChange={handleChange}
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>

        <input
          name="category"
          placeholder="Category"
          value={formData.category}
          onChange={handleChange}
        />

        <input
          name="date"
          type="date"
          value={formData.date}
          onChange={handleChange}
        />

        <button type="submit">Add Transaction</button>
      </form>

      <div className="list">
        {transactions.map((transaction) => (
          <div key={transaction.id} className="list-item">
            <div>
              <h3>{transaction.title}</h3>
              <p>
                {transaction.transaction_type} • KES{" "}
                {transaction.amount.toLocaleString()} •{" "}
                {transaction.category?.name || "Uncategorized"}
              </p>
            </div>

            <button onClick={() => handleDelete(transaction.id)}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}

export default Transactions;