import { api } from "./client";

export const firmwareApi = {
  startBatch: (body, filename) =>
    api.post(
      `/firmware/batch/start-now?filename=${encodeURIComponent(filename)}`,
      body
    ),
  scheduleBatch: (body, filename) =>
    api.post(
      `/firmware/batch/schedule?filename=${encodeURIComponent(filename)}`,
      body
    ),
  getBatchStatus: (workflowId) =>
    api.get(`/firmware/batch/${encodeURIComponent(workflowId)}/status`),
  getDeviceStatus: (workflowId, serialNumber) =>
    api.get(
      `/firmware/batch/${encodeURIComponent(workflowId)}/device/${encodeURIComponent(serialNumber)}/status`
    ),
  pauseBatch: (workflowId) =>
    api.post(`/firmware/batch/${encodeURIComponent(workflowId)}/pause`),
  resumeBatch: (workflowId) =>
    api.post(`/firmware/batch/${encodeURIComponent(workflowId)}/resume`),
  cancelBatch: (workflowId) =>
    api.post(`/firmware/batch/${encodeURIComponent(workflowId)}/cancel`),
};

export const parameterApi = {
  startBatch: (body) => api.post("/parameter-update/batch/start-now", body),
  scheduleBatch: (body) => api.post("/parameter-update/batch/schedule", body),
  getBatchStatus: (workflowId) =>
    api.get(`/parameter-update/batch/${encodeURIComponent(workflowId)}/status`),
  getDeviceStatus: (workflowId, serialNumber) =>
    api.get(
      `/parameter-update/batch/${encodeURIComponent(workflowId)}/device/${encodeURIComponent(serialNumber)}/status`
    ),
  pauseBatch: (workflowId) =>
    api.post(`/parameter-update/batch/${encodeURIComponent(workflowId)}/pause`),
  resumeBatch: (workflowId) =>
    api.post(`/parameter-update/batch/${encodeURIComponent(workflowId)}/resume`),
  cancelBatch: (workflowId) =>
    api.post(`/parameter-update/batch/${encodeURIComponent(workflowId)}/cancel`),
};

export const parameterSetApi = {
  startBatch: (body) => api.post("/parameter-set/batch/start-now", body),
  scheduleBatch: (body) => api.post("/parameter-set/batch/schedule", body),
  getBatchStatus: (workflowId) =>
    api.get(`/parameter-set/batch/${encodeURIComponent(workflowId)}/status`),
  getDeviceStatus: (workflowId, serialNumber) =>
    api.get(
      `/parameter-set/batch/${encodeURIComponent(workflowId)}/device/${encodeURIComponent(serialNumber)}/status`
    ),
  pauseBatch: (workflowId) =>
    api.post(`/parameter-set/batch/${encodeURIComponent(workflowId)}/pause`),
  resumeBatch: (workflowId) =>
    api.post(`/parameter-set/batch/${encodeURIComponent(workflowId)}/resume`),
  cancelBatch: (workflowId) =>
    api.post(`/parameter-set/batch/${encodeURIComponent(workflowId)}/cancel`),
};

export const parameterGetApi = {
  startBatch: (body) => api.post("/parameter-get/batch/start-now", body),
  scheduleBatch: (body) => api.post("/parameter-get/batch/schedule", body),
  getBatchStatus: (workflowId) =>
    api.get(`/parameter-get/batch/${encodeURIComponent(workflowId)}/status`),
  getDeviceStatus: (workflowId, serialNumber) =>
    api.get(
      `/parameter-get/batch/${encodeURIComponent(workflowId)}/device/${encodeURIComponent(serialNumber)}/status`
    ),
  pauseBatch: (workflowId) =>
    api.post(`/parameter-get/batch/${encodeURIComponent(workflowId)}/pause`),
  resumeBatch: (workflowId) =>
    api.post(`/parameter-get/batch/${encodeURIComponent(workflowId)}/resume`),
  cancelBatch: (workflowId) =>
    api.post(`/parameter-get/batch/${encodeURIComponent(workflowId)}/cancel`),
};
