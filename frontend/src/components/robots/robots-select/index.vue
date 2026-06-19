<template>
  <a-select
    v-model="selectedValue"
    v-debounce
    :loading="robotLoading"
    :placeholder="$t('robots.name.select.placeholder')"
    :multiple="props.multiple"
    allow-search
    allow-clear
    @click="getRobotsOptions()"
  >
    <template #label="{ data }">
      <a-space :size="18">
        <a-tag
          v-if="data.value.startsWith('#')"
          :color="tasksTypeColor[data.value.slice(1)]"
        >
          {{ $t(coordinatorName[data.value.slice(1)]) }}
        </a-tag>
        <Media
          v-else
          :style="{
            backgroundColor: 'var(--color-bg-2)',
          }"
          :size="20"
          :url="apiGetRobotsManageAvatarUrl({ name: data.value })"
          scope="avatar"
        />
        {{ data.value.startsWith('#') ? '' : data.label }}
      </a-space>
    </template>
    <a-option v-for="item in robotsOptions" :key="item" :value="item">
      <a-space :size="18">
        <a-tag
          v-if="item.startsWith('#')"
          :color="tasksTypeColor[item.slice(1)]"
        >
          {{ $t(coordinatorName[item.slice(1)]) }}
        </a-tag>
        <Media
          v-else
          :style="{
            backgroundColor: 'var(--color-bg-2)',
          }"
          :size="25"
          :url="apiGetRobotsManageAvatarUrl({ name: item })"
          scope="avatar"
        />
        {{ item.startsWith('#') ? '' : item }}
      </a-space>
    </a-option>
  </a-select>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed, watch } from 'vue';
  import {
    apiGetRobotsManageItems,
    apiGetRobotsManageAvatarUrl,
  } from '@/api/robots/manage';
  import { tasksTypeColor, coordinatorName } from '@/utils/func';
  import Media from '@/components/media/index.vue';

  const props = defineProps<{
    multiple: boolean;
    selectedProjectItem: Record<string, any>;
    scope: 'robot' | 'project';
  }>();

  const selectedRobots = defineModel<string[]>('selectedRobots', {
    default: [],
  });
  const selectedRobot = defineModel<string>('selectedRobot', {
    default: '',
  });

  const selectedValue = computed({
    get: () =>
      props.multiple === true ? selectedRobots.value : selectedRobot.value,
    set: (val: string | string[]) => {
      if (props.multiple === true) {
        selectedRobots.value = val as string[];
      } else {
        selectedRobot.value = val as string;
      }
    },
  });

  const robotLoading = ref(false);

  const robotsOptions = ref<string[]>([]);

  // 获取数字员工选项
  const getRobotsOptions = async () => {
    robotLoading.value = true;
    try {
      if (props.scope === 'robot') {
        const { data } = await apiGetRobotsManageItems({
          page: 0,
        });

        robotsOptions.value = [];
        data.items.forEach((item: Record<string, any>) => {
          robotsOptions.value.push(item.name);
        });
      } else {
        robotsOptions.value =
          props.multiple === true
            ? []
            : ['#agbox-coordinator-sync', '#agbox-coordinator-async'];
        props.selectedProjectItem.history_robots.forEach((item: string) => {
          robotsOptions.value.push(item);
        });
      }

      if (robotsOptions.value.length !== 0) {
        if (props.multiple === false) {
          if (
            selectedRobot.value === '' ||
            robotsOptions.value.find((item) => item === selectedRobot.value) ===
              undefined
          ) {
            [selectedValue.value] = robotsOptions.value;
          }
        } else {
          selectedValue.value = [];
        }
      } else {
        selectedValue.value = props.multiple === false ? '' : [];
      }
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotLoading.value = false;
    }
  };

  onMounted(() => {
    getRobotsOptions().then(() => {
      if (robotsOptions.value.length !== 0) {
        if (props.multiple === false) {
          [selectedValue.value] = robotsOptions.value;
        }
      }
    });
  });

  watch(
    () => props.selectedProjectItem.history_robots,
    () => getRobotsOptions()
  );
</script>
