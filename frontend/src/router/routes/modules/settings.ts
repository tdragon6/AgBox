import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const SETTINGS: AppRouteRecordRaw = {
  path: '/settings',
  name: 'settings',
  component: DEFAULT_LAYOUT,
  redirect: '/settings/index',
  meta: {
    locale: 'menu.settings',
    requiresAuth: true,
    icon: 'icon-settings',
    order: 6,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'index',
      name: 'settingsIndex',
      component: () => import('@/views/settings/index.vue'),
      meta: {
        locale: 'menu.settings',
        requiresAuth: true,
      },
    },
  ],
};

export default SETTINGS;
