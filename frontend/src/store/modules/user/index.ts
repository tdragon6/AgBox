import { defineStore } from 'pinia';
import { apiLogin, apiLogout } from '@/api/auth';
import { setToken, clearToken } from '@/utils/auth';
import { removeRouteListener } from '@/utils/route-listener';

const useUserStore = defineStore('user', {
  state: (): Record<string, any> => ({
    username: localStorage.getItem('username') || undefined,
  }),

  actions: {
    async login(params: Record<string, any>) {
      const { data } = await apiLogin(params);
      setToken(data.token);
      localStorage.setItem('username', data.username);
      this.username = data.username;
    },

    async logout() {
      await apiLogout();
      clearToken();
      localStorage.removeItem('username');
      removeRouteListener();
    },
  },
});

export default useUserStore;
