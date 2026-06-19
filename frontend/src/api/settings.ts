import axios from 'axios';

const API_SUFFIX = '/api/v1/settings';

export function apiGetSettings(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/get`, params);
}

export function apiSetSettings(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/set`, params);
}

export function apiGetSystemInfo() {
  return axios.get(`${API_SUFFIX}/system/info`);
}
