import axios from 'axios';
import qs from 'query-string';
import apiGetBlobUrl from '@/api/blob';

const API_SUFFIX = '/api/v1/files';

export function apiGetTreeNodeData(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/tree`, params);
}

export function apiReadTreeNodeFile(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/read`, params);
}

export function apiSaveTreeNodeFile(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/save`, params);
}

export function apiCreateTreeNodeFile(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/create`, params);
}

export function apiDeleteTreeNodeFile(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiRenameTreeNodeFile(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/rename`, params);
}

export async function apiDownloadDir(params: Record<string, any>) {
  await apiGetBlobUrl(
    `${API_SUFFIX}/dir/download?${qs.stringify(params)}`,
    true
  );
}

export function apiGetFileUrl(params: Record<string, any>) {
  return `${API_SUFFIX}/file/download?${qs.stringify(params)}`;
}

export async function apiDownloadFile(params: Record<string, any>) {
  await apiGetBlobUrl(apiGetFileUrl(params), true);
}

export const UPLOAD_FILE_ENDPOINT = `${
  import.meta.env.VITE_API_BASE_URL
}${API_SUFFIX}/file/upload`;
