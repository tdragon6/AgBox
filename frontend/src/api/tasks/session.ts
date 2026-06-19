import axios from 'axios';

const API_SUFFIX = '/api/v1/tasks/session';

export function apiGetRobotsSessions(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/robots/sessions`, params);
}

export function apiRenameRobotsSessions(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/robots/sessions/rename`, params);
}

export function apiCreateRobotsSessions(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/robots/sessions/create`, params);
}

export function apiDeleteRobotsSessions(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/robots/sessions/delete`, params);
}

export function apiGetRobotsSessionsMessages(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/robots/sessions/messages`, params);
}
