import { createI18n } from 'vue-i18n';
import cn from './zh-CN';
import en from './en-US';

export const LOCALE_OPTIONS = [
  { label: '中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' },
];
const defaultLocale = localStorage.getItem('arco-locale') || 'zh-CN';

const i18n = createI18n({
  locale: defaultLocale,
  fallbackLocale: 'zh-CN',
  legacy: false,
  allowComposition: true,
  messages: {
    'zh-CN': cn,
    'en-US': en,
  },
});

export default i18n;
