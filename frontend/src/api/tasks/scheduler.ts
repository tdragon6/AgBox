import axios from 'axios';

const API_SUFFIX = '/api/v1/tasks/scheduler';

export function apiGetSchedulerItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiCreateScheduler(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/create`, params);
}

export function apiUpdateScheduler(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update`, params);
}

export function apiDeleteScheduler(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiPauseScheduler(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/pause`, params);
}

export function apiResumeScheduler(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/resume`, params);
}
