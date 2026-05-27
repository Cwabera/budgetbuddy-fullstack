import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function Budgets() {
  const [budgets, setBudgets] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    limit_amount: "",
    categories: "",
  });

  async function loadBudgets() {
    const data = await apiRequest("/budgets");
    setBudgets(data);
  }

  useEffect(() => {
    loadBudgets();
  }, []);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      name: formData.name,
      limit_amount: formData.limit_amount,
      categories: formData.categories
        .split(",")
        .map((category) => category.trim())
        .filter(Boolean),
    };

    await apiRequest("/budgets", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    setFormData({
      name: "",
      limit_amount: "",
      categories: "",
    });

    loadBudgets();
  }

  async function handleDelete(id) {
    await apiRequest(`/budgets/${id}`, {
      method: "DELETE",
    });

    loadBudgets();
  }

  return (
    <main className="page">
      <h2>Budgets</h2>

      <form onSubmit={handleSubmit} className="form grid-form">
        <input
          name="name"
          placeholder="Budget name"
          value={formData.name}
          onChange={handleChange}
        />

        <input
          name="limit_amount"
          type="number"
          placeholder="Limit amount"
          value={formData.limit_amount}
          onChange={handleChange}
        />

        <input
          name="categories"
          placeholder="Categories e.g Food, Rent, Transport"
          value={formData.categories}
          onChange={handleChange}
        />

        <button type="submit">Add Budget</button>
      </form>

      <div className="list">
        {budgets.map((budget) => (
          <div key={budget.id} className="list-item">
            <div>
              <h3>{budget.name}</h3>
              <p>KES {budget.limit_amount.toLocaleString()}</p>
              <p>
                Categories:{" "}
                {budget.categories.map((category) => category.name).join(", ")}
              </p>
            </div>

            <button onClick={() => handleDelete(budget.id)}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}

export default Budgets;