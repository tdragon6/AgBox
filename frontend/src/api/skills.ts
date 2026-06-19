import axios from 'axios';

const API_SUFFIX = '/api/v1/skills';

export function apiCreateSkillsCategory(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/category/create`, params);
}

export function apiGetSkillsCategoryItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/category/items`, params);
}

export function apiRenameSkillsCategory(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/category/rename`, params);
}

export function apiDeleteSkillsCategory(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/category/delete`, params);
}

export function apiGetSkillsItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/items`, params);
}

export function apiDeleteSkills(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/delete`, params);
}

export function apiGetSkillsmpItems(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/skillsmp/items`, params);
}

export function apiInstallSkillsmp(params: Record<string, any>) {
  return axios.post(`${API_SUFFIX}/skillsmp/install`, params);
}

export const IMPORT_SKILLS_ENDPOINT = `${
  import.meta.env.VITE_API_BASE_URL
}${API_SUFFIX}/import`;
