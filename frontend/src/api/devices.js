import { api } from "./client";

export const devicesApi = {
  list: () => api.get("/devices"),
  create: (data) => api.post("/devices", data),
  update: (serial, data) => api.put(`/devices/${serial}`, data),
  delete: (serial) => api.delete(`/devices/${serial}`),
};
