import 'vue-router';

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth: boolean;
    icon?: string;
    locale?: string;
    hideInMenu?: boolean;
    hideChildrenInMenu?: boolean;
    order?: number;
  }
}
