import { Link } from "react-router-dom";

function Home() {
  return (
    <main className="page hero">
      <h1>BudgetBuddy</h1>
      <p>Track your income, expenses, budgets, and spending categories.</p>

      <div className="actions">
        <Link to="/register" className="btn">Get Started</Link>
        <Link to="/login" className="btn secondary">Login</Link>
      </div>
    </main>
  );
}

export default Home;