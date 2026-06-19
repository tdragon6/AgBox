<template>
  <a-space size="large">
    <a-form-item :label="$t('tasks.coordinator')" required>
      <a-radio-group v-model="selectedRobot" type="button">
        <a-radio value="#agbox-coordinator-sync">
          {{ $t(coordinatorName['agbox-coordinator-sync']) }}
        </a-radio>
        <a-radio value="#agbox-coordinator-async">
          {{ $t(coordinatorName['agbox-coordinator-async']) }}
        </a-radio>
      </a-radio-group>
    </a-form-item>
    <a-form-item
      v-if="props.projectOptionsSelect === true"
      :label="$t('tasks.project')"
      required
    >
      <a-select
        v-model="selectedProjectName"
        v-debounce
        :loading="projectLoading"
        :placeholder="$t('tasks.project.select.placeholder')"
        allow-search
        allow-clear
        @click="getProjectOptions()"
      >
        <template #label="{ data }">
          <a-space>
            <a-avatar
              :size="20"
              :style="{ backgroundColor: generateColor(data.label) }"
            >
              {{ data.label.charAt(0).toUpperCase() + data.label.charAt(1) }}
            </a-avatar>
            {{ data.label }}
          </a-space>
        </template>
        <a-option
          v-for="item in projectOptions"
          :key="item.id"
          :value="item.id"
          :label="item.name"
        >
          <a-space :size="18">
            <a-avatar
              :size="20"
              :style="{ backgroundColor: generateColor(item.name) }"
            >
              {{ item.name.charAt(0).toUpperCase() + item.name.charAt(1) }}
            </a-avatar>
            {{ item.name }}
          </a-space>
        </a-option>
      </a-select>
    </a-form-item>
  </a-space>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { generateColor } from '@marko19907/string-to-color';
  import { apiGetProjectItems } from '@/api/tasks/project';
  import { coordinatorName } from '@/utils/func';

  const selectedRobot = defineModel<string>('selectedRobot', {
    default: '#agbox-coordinator-sync',
  });

  const selectedProjectItem = defineModel<Record<string, any>>(
    'selectedProjectItem',
    {
      default: {},
    }
  );

  const projectLoading = ref(false);
  const projectOptions = ref<Record<string, any>[]>([]);
  const props = defineProps<{
    projectOptionsSelect: boolean;
  }>();

  const selectedProjectName = computed({
    get: () => {
      if (Object.keys(selectedProjectItem.value).length !== 0) {
        return selectedProjectItem.value.id;
      }
      return '';
    },
    set: (val: string) => {
      const nowItem = projectOptions.value.find((item) => item.id === val);
      if (nowItem !== undefined) {
        selectedProjectItem.value = nowItem;
      } else {
        selectedProjectItem.value = {};
      }
    },
  });

  const getProjectOptions = async () => {
    projectLoading.value = true;
    try {
      const { data } = await apiGetProjectItems({
        page: 0,
      });
      projectOptions.value = data.items;

      if (projectOptions.value.length !== 0) {
        if (Object.keys(selectedProjectItem.value).length === 0) {
          [selectedProjectItem.value] = projectOptions.value;
        } else {
          const nowItem = projectOptions.value.find(
            (item) => item.id === selectedProjectItem.value.id
          );
          if (nowItem === undefined) {
            [selectedProjectItem.value] = projectOptions.value;
          } else {
            selectedProjectItem.value = nowItem;
          }
        }
      } else {
        selectedProjectItem.value = {};
      }
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectLoading.value = false;
    }
  };

  onMounted(() => {
    getProjectOptions();
  });
</script>
