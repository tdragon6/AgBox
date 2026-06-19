<template>
  <a-avatar
    v-if="props.scope === 'avatar' && blobUrl !== ''"
    :style="props.style"
    :size="props.size"
    :trigger-icon-style="{ color: 'var(--color-text-2)' }"
  >
    <template v-if="slots['trigger-icon']" #trigger-icon>
      <slot name="trigger-icon"></slot>
    </template>
    <!-- 确保新值刷新，用 img 标签 -->
    <img :src="blobUrl" />
  </a-avatar>
  <a-spin v-else-if="props.scope === 'image'" :loading="mediaLoading">
    <a-image :src="blobUrl" width="100%" />
  </a-spin>
  <a-spin v-else-if="props.scope === 'video'" :loading="mediaLoading">
    <video :src="blobUrl" controls width="100%"> </video>
  </a-spin>
</template>

<script setup lang="ts">
  import { ref, onMounted, watch, useSlots } from 'vue';
  import apiGetBlobUrl from '@/api/blob';

  const props = defineProps<{
    style: Record<string, any>;
    size: number;
    url: string;
    scope: 'avatar' | 'image' | 'video';
  }>();

  const slots = useSlots();

  const mediaLoading = ref(false);

  const blobUrl = ref<string>('');

  onMounted(async () => {
    if (props.url !== '') {
      mediaLoading.value = true;
      try {
        blobUrl.value = await apiGetBlobUrl(props.url);
      } catch (_) {
        /* eslint-disable no-empty */
      } finally {
        mediaLoading.value = false;
      }
    }
  });

  watch(
    () => props.url,
    async () => {
      if (props.url !== '') {
        mediaLoading.value = true;
        try {
          blobUrl.value = await apiGetBlobUrl(props.url);
        } catch (_) {
          /* eslint-disable no-empty */
        } finally {
          mediaLoading.value = false;
        }
      }
    }
  );
</script>
