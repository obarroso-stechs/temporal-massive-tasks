import { api } from "./client";

export const tasksApi = {
  list: (params = {}) => {
    const qs = Object.entries(params)
      .filter(([, v]) => v != null && v !== "")
      .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
      .join("&");
    return api.get(`/tasks${qs ? `?${qs}` : ""}`);
  },
  getDetail: (taskId) => api.get(`/tasks/${taskId}`),
};
