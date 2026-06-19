import type { Router, LocationQueryRaw } from 'vue-router';

import { useUserStore } from '@/store';
import { isLogin } from '@/utils/auth';

export default function setupUserLoginInfoGuard(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    const userStore = useUserStore();
    if (isLogin() && userStore.username && to.name === 'login') {
      next({
        name: 'Workplace',
        query: {
          ...to.query,
        } as LocationQueryRaw,
      });
    } else if (
      (isLogin() && userStore.username) ||
      to.meta.requiresAuth === false
    ) {
      next();
    } else {
      next({
        name: 'login',
        query: {
          redirect: to.name,
          ...to.query,
        } as LocationQueryRaw,
      });
    }
  });
}
