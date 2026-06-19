import { apiGetSettings, apiSetSettings } from '@/api/settings';
import { Message } from '@arco-design/web-vue';

export async function getSettings(
  name: string,
  defaultValue: string | number | boolean | null
) {
  try {
    const { data } = await apiGetSettings({ name });
    if (
      (name === 'ROBOTS_OVERWRITE' || name === 'SKILLS_OVERWRITE') &&
      data === null
    ) {
      return 'intercept';
    }
    return data;
  } catch (_) {
    return defaultValue;
  }
}

export async function setSettings(
  name: string,
  value: string | number | boolean | null,
  defaultValue: string | number | boolean | null,
  successMessage: string
) {
  try {
    if (
      (name === 'ROBOTS_OVERWRITE' || name === 'SKILLS_OVERWRITE') &&
      value === 'intercept'
    ) {
      value = null;
    }
    await apiSetSettings({ name, value });
    const { data } = await getSettings(name, defaultValue);
    Message.success(successMessage);
    return data;
  } catch (_) {
    return defaultValue;
  }
}
