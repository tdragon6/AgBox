import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const INBOX: AppRouteRecordRaw = {
  path: '/inbox',
  name: 'inbox',
  component: DEFAULT_LAYOUT,
  redirect: '/inbox/index',
  meta: {
    locale: 'menu.inbox',
    requiresAuth: true,
    icon: 'icon-email',
    order: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'index',
      name: 'inboxIndex',
      component: () => import('@/views/inbox/index.vue'),
      meta: {
        locale: 'menu.inbox',
        requiresAuth: true,
      },
    },
  ],
};

export default INBOX;
