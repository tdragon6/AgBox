import axios from 'axios';

const API_SUFFIX = '/api/v1/robots/market';

export function apiGetRobotsMarketItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiInstallRobotsMarket(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/install`, params);
}
