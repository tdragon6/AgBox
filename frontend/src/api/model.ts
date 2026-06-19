import axios from 'axios';

const API_SUFFIX = '/api/v1/model';

export function apiGetModelProvider() {
  return axios.post(`${API_SUFFIX}/provider`);
}

export function apiGetModelBaseUrl(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/base_url`, params);
}

export function apiGetModelList(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/list`, params);
}

export function apiCreateModel(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/create`, params);
}

export function apiUpdateModel(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update`, params);
}

export function apiGetModelItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiDeleteModel(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiGetModelDetail(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/detail`, params);
}
