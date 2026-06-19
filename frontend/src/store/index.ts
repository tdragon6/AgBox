import { createPinia } from 'pinia';
import useAppStore from './modules/app';
import useUserStore from './modules/user';
import useUnreadRobotsInboxCountStore from './modules/inbox';

const pinia = createPinia();

export { useAppStore, useUserStore, useUnreadRobotsInboxCountStore };
export default pinia;
