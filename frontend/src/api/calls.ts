// src/api/calls.ts
import apiClient from "./client";

export interface Call {
  id: number;
  caller_number?: string;
  receiver_number?: string;
  call_status?: string;
  call_duration_seconds?: number;
  should_trigger_automation?: boolean;
  created_at?: string;
}

export const listCalls = async (): Promise<Call[]> => {
  try {
    const response = await apiClient.get<Call[]>("/api/v1/calls");
    return response.data;
  } catch (error) {
    console.error("Error fetching calls data:", error);
    throw error;
  }
};
