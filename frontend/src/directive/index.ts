import { App } from 'vue';
import debounce from './debounce';

export default {
  install(Vue: App) {
    Vue.directive('debounce', debounce);
  },
};
