import { defineStore } from 'pinia';
import defaultSettings from '@/config/settings.json';

const useAppStore = defineStore('app', {
  state: (): Record<string, any> => ({ ...defaultSettings }),

  actions: {
    updateSettings(partial: Partial<Record<string, any>>) {
      // @ts-ignore-next-line
      this.$patch(partial);
    },

    toggleTheme(dark: boolean) {
      if (dark) {
        this.theme = 'dark';
        document.body.setAttribute('arco-theme', 'dark');
      } else {
        this.theme = 'light';
        document.body.removeAttribute('arco-theme');
      }
    },

    toggleDevice(device: string) {
      this.device = device;
    },
  },
});

export default useAppStore;
