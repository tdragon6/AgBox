import axios from 'axios';
import qs from 'query-string';

const API_SUFFIX = '/api/v1/tasks';

export function apiGetTasksItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiGetTasksResult(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/result`, params);
}

export function apiRunTasks(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/run`, params);
}

export function apiCancelTasks(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/cancel`, params);
}

export function apiUpdateTasksPriority(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update/priority`, params);
}

export function apiGetTasksMessages(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/messages`, params);
}

export const UPLOAD_PASTE_IMAGE_ENDPOINT = `${
  import.meta.env.VITE_API_BASE_URL
}${API_SUFFIX}/paste/upload`;

export function apiGetPasteImageUrl(params: Record<string, any>) {
  return `${API_SUFFIX}/paste?${qs.stringify(params)}`;
}
