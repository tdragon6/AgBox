<template>
  <a-card
    :style="{ height: props.scope === 'inbox' ? '88vh' : '30vh' }"
    :title="$t('inbox')"
  >
    <a-menu
      v-model:selected-keys="selectedRobotsNames"
      class="custom-overflow-80vh"
      :style="props.scope === 'dashboard' ? { height: '22vh' } : {}"
    >
      <Empty v-if="unreadRobotsInboxCount.length === 0" />
      <a-menu-item
        v-for="item in unreadRobotsInboxCount"
        v-else
        :key="item.coordinator === true ? `#${item.robot}` : item.robot"
        @click="
          if (props.scope === 'dashboard') {
            router.push({
              name: 'inboxIndex',
              query: {
                robot:
                  item.coordinator === true ? `#${item.robot}` : item.robot,
              },
            });
          }
        "
      >
        <template #icon>
          <a-avatar
            v-if="item.coordinator === true"
            :size="30"
            :style="{ backgroundColor: generateColor(item.robot) }"
          >
            #
          </a-avatar>
          <Media
            v-else
            :style="{
              backgroundColor: 'var(--color-bg-2)',
            }"
            :size="30"
            :url="apiGetRobotsManageAvatarUrl({ name: item.robot })"
            scope="avatar"
          />
        </template>
        <a-tooltip v-if="item.overflow === true" :content="item.robot">
          <a-tag
            v-if="item.coordinator === true"
            :color="tasksTypeColor[item.robot]"
          >
            {{ $t(coordinatorName[item.robot]) }}
          </a-tag>
          <span
            v-else
            class="custom-ellipsis"
            @mouseenter="checkTitleOverflow($event, item)"
          >
            {{ item.robot }}
          </span>
        </a-tooltip>
        <div v-else>
          <a-tag
            v-if="item.coordinator === true"
            :color="tasksTypeColor[item.robot]"
          >
            {{ $t(coordinatorName[item.robot]) }}
          </a-tag>
          <span
            v-else
            class="custom-ellipsis"
            @mouseenter="checkTitleOverflow($event, item)"
          >
            {{ item.robot }}
          </span>
        </div>
        <a-badge :count="item.count" :max-count="99" style="margin-left: auto">
        </a-badge>
      </a-menu-item>
    </a-menu>
  </a-card>
</template>

<script setup lang="ts">
  import { computed, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import Empty from '@/components/empty/index.vue';
  import { generateColor } from '@marko19907/string-to-color';
  import {
    checkTitleOverflow,
    tasksTypeColor,
    coordinatorName,
  } from '@/utils/func';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import useUnreadRobotsInboxCountStore from '@/store/modules/inbox';
  import Media from '@/components/media/index.vue';

  const router = useRouter();
  const route = useRoute();

  const unreadRobotsInboxCountStore = useUnreadRobotsInboxCountStore();

  const props = defineProps<{
    scope: 'inbox' | 'dashboard';
  }>();

  const selectedRobotsNames = defineModel<string[]>('selectedRobotsNames', {
    default: [],
  });

  const unreadRobotsInboxCount = computed(() => {
    if (props.scope === 'dashboard') {
      return unreadRobotsInboxCountStore.data.filter(
        (item) => item.count !== 0
      );
    }
    return unreadRobotsInboxCountStore.data;
  });

  onMounted(async () => {
    await unreadRobotsInboxCountStore.getUnreadRobotsInboxCount();

    if (
      props.scope === 'inbox' &&
      route.query.robot === undefined &&
      unreadRobotsInboxCount.value.length !== 0
    ) {
      const defaultItem = unreadRobotsInboxCount.value[0];

      selectedRobotsNames.value = [
        defaultItem.coordinator === true
          ? `#${defaultItem.robot}`
          : defaultItem.robot,
      ];
    }
  });
</script>

<style scoped lang="less">
  :deep(.arco-menu-title .arco-trigger) {
    display: flex;
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }

  :deep(.arco-menu-title) {
    display: flex;
    align-items: center;
  }

  :deep(.arco-menu-item:hover) .custom-action-icon {
    opacity: 1;
  }
</style>
