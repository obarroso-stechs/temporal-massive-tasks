import { api } from "./client";

export const reportsApi = {
  list: () => api.get("/reports"),
  getById: (id) => api.get(`/reports/${id}`),
  generate: (taskId, format, force = false) =>
    api.post(
      `/reports/generate?task_id=${encodeURIComponent(taskId)}&report_format=${format}&force=${force}`,
      null
    ),
  delete: (id) => api.delete(`/reports/${id}`),
  downloadUrl: (id) => `/api/reports/${id}/download`,
};
