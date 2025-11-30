import api from "./client";

export interface Product {
  id: number;
  name: string;
  category: string | null;
  gender: string | null;
  tags: string | null;
  price: number;
  description: string | null;
  image_url: string | null;
  is_active: boolean;
}

export async function listProducts(): Promise<Product[]> {
  const { data } = await api.get<Product[]>("/products/");
  return data;
}
