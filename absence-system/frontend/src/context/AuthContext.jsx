import { createContext, useContext, useMemo, useState } from "react";
import { api } from "../api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("absence_user");
    return saved ? JSON.parse(saved) : null;
  });

  async function login(email, password) {
    const { data } = await api.post("/auth/login", { email, password });
    localStorage.setItem("absence_token", data.token);
    localStorage.setItem("absence_user", JSON.stringify(data.user));
    setUser(data.user);
  }

  function demoLogin(role = "admin") {
    const demoUser = {
      id: "demo",
      name: role === "admin" ? "Admin Director" : "Professor Lina",
      role,
      department: role === "admin" ? "Academic Affairs" : "Computer Science"
    };
    localStorage.setItem("absence_token", "demo-token");
    localStorage.setItem("absence_user", JSON.stringify(demoUser));
    setUser(demoUser);
  }

  function logout() {
    localStorage.removeItem("absence_token");
    localStorage.removeItem("absence_user");
    setUser(null);
  }

  const value = useMemo(() => ({ user, login, demoLogin, logout }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
