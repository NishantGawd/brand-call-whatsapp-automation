// src/api/automationSettings.ts
import apiClient from "./client";

export interface AutomationSettings {
  enabled: boolean;
  min_call_duration_seconds: number;
}

export const getAutomationSettings = async (): Promise<AutomationSettings> => {
  try {
    const response = await apiClient.get<AutomationSettings>(
      "/api/v1/settings/automation"
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching automation settings:", error);
    throw error;
  }
};

export const updateAutomationSettings = async (
  settings: Partial<AutomationSettings>
): Promise<AutomationSettings> => {
  try {
    const response = await apiClient.put<AutomationSettings>(
      "/api/v1/settings/automation",
      settings
    );
    return response.data;
  } catch (error) {
    console.error("Error updating automation settings:", error);
    throw error;
  }
};
