<template>
  <a-form-item :label="$t('tasks.session.select.placeholder')" required>
    <a-spin :loading="robotsSessionsLoading">
      <a-dropdown @click="getRobotsSessionsOptions">
        <a-button>
          <a-space
            >{{ $t('tasks.session.select.placeholder') }}
            <icon-down />
          </a-space>
        </a-button>
        <template #content>
          <a-dsubmenu
            v-for="robot in robotsOptions"
            :key="robot"
            :value="robot"
          >
            <template #default>
              <Media
                :style="{
                  backgroundColor: 'var(--color-bg-2)',
                }"
                :size="20"
                :url="apiGetRobotsManageAvatarUrl({ name: robot })"
                scope="avatar"
              />
              {{ robot }}
            </template>
            <template #content>
              <div v-if="sessionOptions[robot].length !== 0">
                <a-doption
                  v-for="session in sessionOptions[robot]"
                  :key="session.id"
                  :value="session.id"
                  @click="
                    selectedRobot = robot;
                    selectedSessionItem = session;
                  "
                >
                  <a-space>
                    <a-avatar
                      :size="20"
                      :style="{ backgroundColor: generateColor(session.title) }"
                    >
                      {{
                        session.title.charAt(0).toUpperCase() +
                        session.title.charAt(1)
                      }}
                    </a-avatar>
                    {{ session.title }}
                  </a-space>
                </a-doption>
              </div>
              <Empty v-else style="padding: 20px" />
            </template>
          </a-dsubmenu>
        </template>
      </a-dropdown>
    </a-spin>
  </a-form-item>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import {
    apiGetRobotsManageItems,
    apiGetRobotsManageAvatarUrl,
  } from '@/api/robots/manage';
  import { generateColor } from '@marko19907/string-to-color';
  import { apiGetRobotsSessions } from '@/api/tasks/session';
  import Empty from '@/components/empty/index.vue';
  import Media from '@/components/media/index.vue';

  const selectedRobot = defineModel<string>('selectedRobot', {
    default: '',
  });
  const selectedSessionItem = defineModel<Record<string, any>>(
    'selectedSessionItem',
    {
      default: {},
    }
  );

  const robotsSessionsLoading = ref(false);

  const robotsOptions = ref<string[]>([]);
  const sessionOptions = ref<Record<string, any[]>>({});

  const getSessionsOptions = async (robot: string) => {
    try {
      const { data } = await apiGetRobotsSessions({
        name: robot,
        page: 0,
      });
      sessionOptions.value[robot] = data;
    } catch (_) {
      /* eslint-disable no-empty */
    }
  };

  const getRobotsSessionsOptions = async () => {
    robotsSessionsLoading.value = true;
    try {
      const { data } = await apiGetRobotsManageItems({ page: 0 });
      robotsOptions.value = [];
      data.items.forEach(async (item: Record<string, any>) => {
        robotsOptions.value.push(item.name);
        sessionOptions.value[item.name] = [];
        await getSessionsOptions(item.name);
      });
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsSessionsLoading.value = false;
    }
  };
</script>
