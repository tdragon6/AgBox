import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const TASKS: AppRouteRecordRaw = {
  path: '/tasks',
  name: 'tasks',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.tasks',
    requiresAuth: true,
    icon: 'icon-ordered-list',
    order: 3,
  },
  children: [
    {
      path: 'session',
      name: 'Session',
      component: () => import('@/views/tasks/session/index.vue'),
      meta: {
        locale: 'menu.tasks.session',
        requiresAuth: true,
      },
    },
    {
      path: 'project',
      name: 'Project',
      component: () => import('@/views/tasks/project/index.vue'),
      meta: {
        locale: 'menu.tasks.project',
        requiresAuth: true,
      },
    },
    {
      path: 'scheduler',
      name: 'Scheduler',
      component: () => import('@/views/tasks/scheduler/index.vue'),
      meta: {
        locale: 'menu.tasks.scheduler',
        requiresAuth: true,
      },
    },
  ],
};

export default TASKS;
