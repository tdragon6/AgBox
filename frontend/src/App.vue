<template>
  <a-config-provider :locale="locale">
    <router-view />
  </a-config-provider>
</template>

<script setup lang="ts">
  import { computed, watch, onMounted } from 'vue';
  import enUS from '@arco-design/web-vue/es/locale/lang/en-us';
  import zhCN from '@arco-design/web-vue/es/locale/lang/zh-cn';
  import { useIntervalFn } from '@vueuse/core';
  import useLocale from '@/hooks/locale';
  import useUserStore from '@/store/modules/user';
  import useUnreadRobotsInboxCountStore from '@/store/modules/inbox';
  import { isLogin } from '@/utils/auth';

  const userStore = useUserStore();
  const unreadRobotsInboxCount = useUnreadRobotsInboxCountStore();

  const { currentLocale } = useLocale();
  const locale = computed(() => {
    switch (currentLocale.value) {
      case 'zh-CN':
        return zhCN;
      case 'en-US':
        return enUS;
      default:
        return enUS;
    }
  });

  const { pause, resume } = useIntervalFn(
    () => unreadRobotsInboxCount.getUnreadRobotsInboxCount(),
    10000,
    { immediate: false, immediateCallback: true }
  );

  onMounted(() => {
    if (isLogin() && userStore.username) {
      resume();
    }
  });

  watch(
    () => userStore.username,
    (username) => {
      if (isLogin() && username) {
        resume();
      } else {
        pause();
      }
    }
  );
</script>
