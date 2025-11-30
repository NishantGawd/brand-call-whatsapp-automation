// src/api/auth.ts
import axios from "axios";

// BASE URL for your FastAPI backend
// Adjust if you use a different host/port or env variable.
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  // IMPORTANT: no withCredentials here – we use token-based auth, not cookies
  // withCredentials: true,
});

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// This should match whatever your /users/me returns
export interface CurrentUser {
  id: number;
  email: string;
  full_name?: string | null;
  tenant_id?: number | null;
  is_active: boolean;
  // add other fields if your backend returns them
}

/**
 * Call FastAPI /auth/login
 * Body must be x-www-form-urlencoded with fields:
 * - username
 * - password
 */
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const { data } = await api.post<LoginResponse>(
    "/auth/login",
    form.toString(),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return data;
}

/**
 * Fetch current user info using the JWT access token
 * GET /users/me with Authorization: Bearer <token>
 */
export async function fetchCurrentUser(token: string): Promise<CurrentUser> {
  const { data } = await api.get<CurrentUser>("/users/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return data;
}
