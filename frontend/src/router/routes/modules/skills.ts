import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const SKILLS: AppRouteRecordRaw = {
  path: '/skills',
  name: 'skills',
  component: DEFAULT_LAYOUT,
  redirect: '/skills/index',
  meta: {
    locale: 'menu.skills',
    requiresAuth: true,
    icon: 'icon-tool',
    order: 4,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'index',
      name: 'skillsIndex',
      component: () => import('@/views/skills/index.vue'),
      meta: {
        locale: 'menu.skills',
        requiresAuth: true,
      },
    },
  ],
};

export default SKILLS;
