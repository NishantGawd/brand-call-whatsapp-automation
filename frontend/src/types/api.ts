export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface CurrentUser {
  id: number;
  email: string;
  full_name: string | null;
  role: string | null;
  tenant_id: number | null;
}
