<template>
  <div class="navbar">
    <div class="left-side">
      <a-space>
        <a-image src="/logo.svg" width="30px" />
        <a-typography-title
          :style="{ margin: 0, fontSize: '18px' }"
          :heading="5"
        >
          AgBox
        </a-typography-title>
        <icon-menu-fold
          v-if="appStore.device === 'mobile'"
          style="font-size: 22px; cursor: pointer"
          @click="toggleDrawerMenu"
        />
      </a-space>
    </div>
    <ul class="right-side">
      <li>
        <a-tooltip :content="$t('common.create')">
          <a-button
            class="nav-btn"
            type="outline"
            :shape="'circle'"
            @click="createTasksModalVisible = true"
          >
            <template #icon>
              <icon-plus />
            </template>
          </a-button>
        </a-tooltip>
      </li>
      <li>
        <a-tooltip :content="$t('settings.language')">
          <a-button
            class="nav-btn"
            type="outline"
            :shape="'circle'"
            @click="setDropDownVisible"
          >
            <template #icon>
              <icon-language />
            </template>
          </a-button>
        </a-tooltip>
        <a-dropdown trigger="click" @select="changeLocale as any">
          <div ref="triggerBtn" class="trigger-btn"></div>
          <template #content>
            <a-doption
              v-for="item in locales"
              :key="item.value"
              :value="item.value"
            >
              <template #icon>
                <icon-check v-show="item.value === currentLocale" />
              </template>
              {{ item.label }}
            </a-doption>
          </template>
        </a-dropdown>
      </li>
      <li>
        <a-tooltip
          :content="
            theme === 'light'
              ? $t('navbar.theme.toDark')
              : $t('navbar.theme.toLight')
          "
        >
          <a-button
            class="nav-btn"
            type="outline"
            :shape="'circle'"
            @click="handleToggleTheme"
          >
            <template #icon>
              <icon-moon-fill v-if="theme === 'dark'" />
              <icon-sun-fill v-else />
            </template>
          </a-button>
        </a-tooltip>
      </li>
      <li>
        <a-tooltip :content="$t('inbox')">
          <a-badge :count="inboxCount">
            <a-button
              class="nav-btn"
              type="outline"
              :shape="'circle'"
              @click="setPopoverVisible"
            >
              <icon-notification />
            </a-button>
          </a-badge>
        </a-tooltip>
        <a-popover
          trigger="click"
          :arrow-style="{ display: 'none' }"
          :content-style="{ padding: 0, minWidth: '400px' }"
          content-class="message-popover"
        >
          <div ref="refBtn" class="ref-btn"></div>
          <template #content>
            <InboxItems scope="dashboard" />
          </template>
        </a-popover>
      </li>
      <li>
        <a-tooltip
          :content="
            isFullscreen
              ? $t('navbar.screen.toExit')
              : $t('navbar.screen.toFull')
          "
        >
          <a-button
            class="nav-btn"
            type="outline"
            :shape="'circle'"
            @click="toggleFullScreen"
          >
            <template #icon>
              <icon-fullscreen-exit v-if="isFullscreen" />
              <icon-fullscreen v-else />
            </template>
          </a-button>
        </a-tooltip>
      </li>
      <li>
        <a-dropdown trigger="click">
          <a-avatar
            :size="32"
            :style="{ marginRight: '8px', cursor: 'pointer' }"
          >
            <img src="/images/tdragon6.jpg" width="30px" />
          </a-avatar>
          <template #content>
            <a-doption>
              <a-space @click="visitUrl('https://github.com/tdragon6/AgBox')">
                <icon-github />
                {{ $t('dashboard.docs.repoUrl') }}
              </a-space>
            </a-doption>
            <a-doption>
              <a-space
                @click="visitUrl('https://tdragon6.github.io/AgBox-Docs')"
              >
                <icon-question-circle />
                {{ $t('dashboard.docs') }}
              </a-space>
            </a-doption>
            <a-doption>
              <a-space @click="visitUrl(`${rootUrl}/docs`)">
                <icon-link />
                {{ $t('navbar.docs.api') }}
              </a-space>
            </a-doption>
            <a-doption>
              <a-space @click="logout">
                <icon-export />
                {{ $t('navbar.logout') }}
              </a-space>
            </a-doption>
          </template>
        </a-dropdown>
      </li>
    </ul>
  </div>
  <TasksInput
    v-if="createTasksModalVisible === true"
    :session-item="{}"
    :robot="''"
    @close="createTasksModalVisible = false"
  />
</template>

<script setup lang="ts">
  import { computed, ref, inject } from 'vue';
  import { useDark, useToggle, useFullscreen } from '@vueuse/core';
  import { useAppStore, useUserStore } from '@/store';
  import { LOCALE_OPTIONS } from '@/locale';
  import useLocale from '@/hooks/locale';
  import TasksInput from '@/components/tasks/tasks-input/index.vue';
  import InboxItems from '@/views/inbox/components/inbox-items.vue';
  import useUnreadRobotsInboxCountStore from '@/store/modules/inbox';
  import { visitUrl } from '@/utils/func';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';

  const rootUrl = computed(() => {
    return window.location.origin;
  });

  const unreadRobotsInboxCountStore = useUnreadRobotsInboxCountStore();
  const inboxCount = computed(() => {
    let count = 0;
    unreadRobotsInboxCountStore.data.forEach((item) => {
      count += item.count;
    });
    return count;
  });

  const appStore = useAppStore();
  const { changeLocale, currentLocale } = useLocale();
  const { isFullscreen, toggle: toggleFullScreen } = useFullscreen();
  const locales = [...LOCALE_OPTIONS];

  const createTasksModalVisible = ref(false);

  const theme = computed(() => {
    return appStore.theme;
  });

  const isDark = useDark({
    selector: 'body',
    attribute: 'arco-theme',
    valueDark: 'dark',
    valueLight: 'light',
    storageKey: 'arco-theme',
    onChanged(dark: boolean) {
      appStore.toggleTheme(dark);
    },
  });
  const toggleTheme = useToggle(isDark);
  const handleToggleTheme = () => {
    toggleTheme();
  };

  const refBtn = ref();
  const triggerBtn = ref();

  const setPopoverVisible = () => {
    const event = new MouseEvent('click', {
      view: window,
      bubbles: true,
      cancelable: true,
    });
    refBtn.value.dispatchEvent(event);
  };

  const setDropDownVisible = () => {
    const event = new MouseEvent('click', {
      view: window,
      bubbles: true,
      cancelable: true,
    });
    triggerBtn.value.dispatchEvent(event);
  };

  const toggleDrawerMenu = inject('toggleDrawerMenu') as () => void;

  const router = useRouter();
  const { t } = useI18n();
  const userStore = useUserStore();

  const logout = async () => {
    try {
      await userStore.logout();
      const currentRoute = router.currentRoute.value;
      Message.success(t('navbar.logout.success'));
      router.push({
        name: 'login',
        query: {
          ...router.currentRoute.value.query,
          redirect: currentRoute.name as string,
        },
      });
    } catch (_) {
      /* eslint-disable no-empty */
    }
  };
</script>

<style scoped lang="less">
  .navbar {
    display: flex;
    justify-content: space-between;
    height: 100%;
    background-color: var(--color-bg-2);
    border-bottom: 1px solid var(--color-border);
  }

  .left-side {
    display: flex;
    align-items: center;
    padding-left: 20px;
  }

  .center-side {
    flex: 1;
  }

  .right-side {
    display: flex;
    padding-right: 20px;
    list-style: none;
    :deep(.locale-select) {
      border-radius: 20px;
    }
    li {
      display: flex;
      align-items: center;
      padding: 0 10px;
    }

    a {
      color: var(--color-text-1);
      text-decoration: none;
    }
    .nav-btn {
      border-color: rgb(var(--gray-2));
      color: rgb(var(--gray-8));
      font-size: 16px;
    }
    .trigger-btn,
    .ref-btn {
      position: absolute;
      bottom: 14px;
    }
    .trigger-btn {
      margin-left: 14px;
    }
  }
</style>

<style lang="less">
  .message-popover {
    .arco-popover-content {
      margin-top: 0;
    }
  }
</style>
