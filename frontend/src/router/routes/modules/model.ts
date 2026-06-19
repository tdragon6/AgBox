import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const MODEL: AppRouteRecordRaw = {
  path: '/model',
  name: 'model',
  component: DEFAULT_LAYOUT,
  redirect: '/model/index',
  meta: {
    locale: 'menu.model',
    requiresAuth: true,
    icon: 'icon-tag',
    order: 5,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'index',
      name: 'modelIndex',
      component: () => import('@/views/model/index.vue'),
      meta: {
        locale: 'menu.model',
        requiresAuth: true,
      },
    },
  ],
};

export default MODEL;
