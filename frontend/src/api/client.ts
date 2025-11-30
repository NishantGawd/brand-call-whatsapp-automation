// src/api/client.ts
import axios from "axios";

const client = axios.create({
  baseURL: "/api/v1",
});

// Attach JWT token from localStorage (set by AuthContext/auth.ts)
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    // FastAPI expects standard bearer token header
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
