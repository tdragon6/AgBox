import axios from 'axios';

const API_SUFFIX = '/api/v1/inbox';

export function apiGetRobotsInboxUnreadCount() {
  return axios.get(`${API_SUFFIX}/robots/count/unread`);
}

export function apiGetInboxItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiDeleteInbox(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiUpdateInboxReadStatus(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update/read/status`, params);
}
