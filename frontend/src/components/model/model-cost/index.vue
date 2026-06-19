<template>
  <a-descriptions
    :data="modelCostDetail"
    layout="inline-vertical"
    size="large"
    bordered
  />
</template>

<script setup lang="ts">
  import { computed } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { DescData } from '@arco-design/web-vue';

  const { t } = useI18n();

  const props = defineProps<{
    includedModelCostItem: Record<string, any>;
  }>();

  const modelCostDetail = computed(() => {
    const keys = [
      'inputTokens',
      'outputTokens',
      'cacheReadTokens',
      'cacheWriteTokens',
      'reasoningTokens',
      'estimatedCostUsd',
      'actualCostUsd',
    ];

    const result: DescData[] = [];

    keys.forEach((key) => {
      result.push({
        label: t(`model.cost.${key}`),
        value: props.includedModelCostItem[key],
      });
    });
    return result;
  });
</script>
