import { createContext, useContext, useEffect, useState } from "react";
import { apiRequest } from "../services/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function register(formData) {
    const data = await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(formData),
    });

    localStorage.setItem("token", data.token);
    setUser(data.user);
  }

  async function login(formData) {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify(formData),
    });

    localStorage.setItem("token", data.token);
    setUser(data.user);
  }

  function logout() {
    localStorage.removeItem("token");
    setUser(null);
  }

  useEffect(() => {
    async function checkUser() {
      const token = localStorage.getItem("token");

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await apiRequest("/auth/me");
        setUser(currentUser);
      } catch {
        localStorage.removeItem("token");
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    checkUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}