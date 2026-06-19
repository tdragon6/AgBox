import type { Router } from 'vue-router';
import { setRouteEmitter } from '@/utils/route-listener';
import NProgress from 'nprogress';
import setupUserLoginInfoGuard from './userLoginInfo';

function setupPageGuard(router: Router) {
  router.beforeEach(async (to) => {
    NProgress.start();
    setRouteEmitter(to);
  });
}

export default function createRouteGuard(router: Router) {
  setupPageGuard(router);
  setupUserLoginInfoGuard(router);
}
