import axios from 'axios';

export function apiLogin(params: Record<string, any>) {
  return axios.post('/api/v1/auth/login', params);
}

export function apiLogout() {
  return axios.post('/api/v1/auth/logout');
}
