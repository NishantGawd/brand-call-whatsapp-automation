// src/context/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import { login as apiLogin, fetchCurrentUser } from "../api/auth";
import type { CurrentUser } from "../api/auth";

interface AuthContextValue {
  token: string | null;
  user: CurrentUser | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

const AUTH_TOKEN_KEY = "auth_token";

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem(AUTH_TOKEN_KEY)
  );
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // On first load: if there's a token, try to fetch the current user
  useEffect(() => {
    const storedToken = localStorage.getItem(AUTH_TOKEN_KEY);
    if (!storedToken) return;

    setIsLoading(true);
    setError(null);

    fetchCurrentUser(storedToken)
      .then((me) => {
        setToken(storedToken);
        setUser(me);
      })
      .catch((err) => {
        console.error("Failed to load user from stored token:", err);
        localStorage.removeItem(AUTH_TOKEN_KEY);
        setToken(null);
        setUser(null);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  const handleLogin = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // 1) Get token from /auth/login
      const data = await apiLogin(email, password);
      const newToken = data.access_token;

      // 2) Persist token
      localStorage.setItem(AUTH_TOKEN_KEY, newToken);
      setToken(newToken);

      // 3) Fetch user
      const me = await fetchCurrentUser(newToken);
      setUser(me);
    } catch (err) {
      console.error("Login failed:", err);
      setError("Invalid email or password. Please try again.");
      localStorage.removeItem(AUTH_TOKEN_KEY);
      setToken(null);
      setUser(null);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    setToken(null);
    setUser(null);
    setError(null);
  };

  const value: AuthContextValue = {
    token,
    user,
    isLoading,
    error,
    login: handleLogin,
    logout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
};
