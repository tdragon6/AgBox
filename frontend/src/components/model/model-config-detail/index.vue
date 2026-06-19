<template>
  <a-card :bordered="false">
    <template #title>
      <a-space :size="18">
        <a-avatar :style="{ backgroundColor: 'var(--color-bg-2)' }">
          <!-- 确保新值刷新，用 img 标签 -->
          <img
            :src="`/images/provider/${
              props.modelDetail.provider_id.split('-')[0]
            }.svg`"
          />
        </a-avatar>
        <span style="font-size: 20px">
          {{ props.modelDetail.provider_id }}
        </span>
        <a-badge
          :status="props.modelDetail.is_online ? 'success' : 'normal'"
          :text="
            props.modelDetail.is_online
              ? $t('common.online')
              : $t('common.offline')
          "
        />
      </a-space>
    </template>
    <template #actions>
      <span> </span>
    </template>
    <a-space direction="vertical">
      <a-typography-text type="secondary" style="font-size: 15px">
        {{ props.modelDetail.base_url }}
      </a-typography-text>
      <a-tag color="magenta" bordered size="small">
        <template #icon> <icon-robot /> </template>
        {{ props.modelDetail.model }}
      </a-tag>
      <a-tag color="arcoblue" bordered size="small">
        <template #icon> <icon-at /> </template>
        {{ props.modelDetail.api_key }}
      </a-tag>
    </a-space>
    <a-card-meta>
      <template #avatar>
        {{
          dayjs(props.modelDetail.updated_time).format('YYYY-MM-DD HH:mm:ss')
        }}
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup lang="ts">
  import dayjs from 'dayjs';

  const props = defineProps<{ modelDetail: Record<string, any> }>();
</script>

<style scoped lang="less">
  :deep(.arco-card-header) {
    height: auto;
    border: none;
  }
</style>
