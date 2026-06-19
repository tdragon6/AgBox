<template>
  <a-select
    v-model="selectedPriority"
    :placeholder="$t('tasks.priority.placeholder')"
    allow-clear
    :multiple="props.multiple"
  >
    <template v-if="props.multiple === false" #label>
      <a-tag :color="tasksPriorityColor[selectedPriority]">
        {{ selectedPriority }}
      </a-tag>
    </template>
    <a-option
      v-for="item in tasksPriorityOptions"
      :key="item.value"
      :value="item.value"
      :tag-props="{ color: tasksPriorityColor[item.value] }"
    >
      <a-tag :color="tasksPriorityColor[item.value]">
        {{ item.label }}
      </a-tag>
    </a-option>
  </a-select>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { tasksPriorityColor } from '@/utils/func';

  const props = defineProps<{ multiple: boolean }>();

  const selectedPriority = defineModel<string>('selectedPriority', {
    default: 'P3',
  });

  const tasksPriorityOptions = ref(
    Array.from({ length: 4 }, (_, i) => ({
      label: `P${i + 1}`,
      value: `P${i + 1}`,
    }))
  );
</script>
