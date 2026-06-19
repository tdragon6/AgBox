import axios from 'axios';
import qs from 'query-string';
import apiGetBlobUrl from '@/api/blob';

const API_SUFFIX = '/api/v1/robots/manage';

export function apiGetRobotsManageItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiCreateRobotsManage(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/create`, params);
}

export function apiUpdateRobotsManage(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/update`, params);
}

export function apiDeleteRobotsManage(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiCloneRobotsManage(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/clone`, params);
}

export async function apiDownloadRobotsManage(params: Record<string, any>) {
  await apiGetBlobUrl(`${API_SUFFIX}/download?${qs.stringify(params)}`, true);
}

export function apiGetRobotsManageAvatarUrl(params: Record<string, any>) {
  if (params.name === '' || params.name === undefined) {
    return '';
  }
  return `${API_SUFFIX}/avatar?${qs.stringify(params)}&_t=${Date.now()}`;
}

export const IMPORT_ROBOTS_MANAGE_ENDPOINT = `${
  import.meta.env.VITE_API_BASE_URL
}${API_SUFFIX}/import`;

export function apiGetRobotsManageModelDetail(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/model/config`, params);
}

export function apiSaveRobotsManageModelDetail(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/model/config/save`, params);
}

export function apiRobotImportSkills(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/skills/import`, params);
}

export const UPLOAD_ROBOTS_MANAGE_AVATAR_ENDPOINT = `${
  import.meta.env.VITE_API_BASE_URL
}${API_SUFFIX}/avatar/upload`;

export function apiReadRobotsManageRule(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/rule/read`, params);
}

export function apiSaveRobotsManageRule(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/rule/save`, params);
}

export function apiReadRobotsManageMemory(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/memory/read`, params);
}

export function apiSaveRobotsManageMemory(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/memory/save`, params);
}

export function apiReadRobotsManageConfig(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/config/read`, params);
}

export function apiSaveRobotsManageConfig(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/config/save`, params);
}

export function apiReadRobotsManageEnv(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/env/read`, params);
}

export function apiSaveRobotsManageEnv(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/env/save`, params);
}
