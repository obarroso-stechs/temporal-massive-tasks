import { api } from "./client";

export const groupsApi = {
  list: () => api.get("/device-groups"),
  create: (data) => api.post("/device-groups", data),
  update: (id, data) => api.put(`/device-groups/${id}`, data),
  delete: (id) => api.delete(`/device-groups/${id}`),
  assignDevices: (id, deviceIds) =>
    api.post(`/device-groups/${id}/devices`, { device_ids: deviceIds }),
  removeDevice: (groupId, deviceId) =>
    api.delete(`/device-groups/${groupId}/devices/${deviceId}`),
};
