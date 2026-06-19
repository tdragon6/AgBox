import axios from 'axios';

const API_SUFFIX = '/api/v1/tasks/project';

export function apiGetProjectItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiCreateProject(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/create`, params);
}

export function apiUpdateProject(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update`, params);
}

export function apiDeleteProject(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}
