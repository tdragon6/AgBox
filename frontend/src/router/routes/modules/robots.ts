import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const ROBOTS: AppRouteRecordRaw = {
  path: '/robots',
  name: 'robots',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.robots',
    requiresAuth: true,
    icon: 'icon-robot',
    order: 2,
  },
  children: [
    {
      path: 'manage',
      name: 'robotsManage',
      component: () => import('@/views/robots/manage/index.vue'),
      meta: {
        locale: 'menu.robots.manage',
        requiresAuth: true,
      },
    },
    {
      path: 'market',
      name: 'robotsMarket',
      component: () => import('@/views/robots/market/index.vue'),
      meta: {
        locale: 'menu.robots.market',
        requiresAuth: true,
      },
    },
  ],
};

export default ROBOTS;
