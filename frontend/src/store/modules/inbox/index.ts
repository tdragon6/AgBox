import { defineStore } from 'pinia';
import { apiGetRobotsInboxUnreadCount } from '@/api/inbox';

const useUnreadRobotsInboxCountStore = defineStore('unreadRobotsInboxCount', {
  state: (): Record<string, any[]> => ({
    data: [],
  }),

  actions: {
    async getUnreadRobotsInboxCount() {
      try {
        const { data } = await apiGetRobotsInboxUnreadCount();

        this.$reset();
        this.data = data;
      } catch (_) {
        /* eslint-disable no-empty */
      }
    },
  },
});

export default useUnreadRobotsInboxCountStore;
