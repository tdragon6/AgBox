<template>
  <a-card>
    <template #actions>
      <a-tooltip :content="$t('dashboard.author.github')">
        <icon-user
          v-debounce
          class="custom-icon-button"
          @click="visitUrl('https://github.com/tdragon6')"
        />
      </a-tooltip>
      <a-tooltip :content="$t('dashboard.author.star')">
        <icon-thumb-up
          v-debounce
          class="custom-icon-button"
          @click="visitUrl('https://github.com/tdragon6/AgBox#star')"
        />
      </a-tooltip>
    </template>
    <div style="display: flex; justify-content: center; padding: 31px 0">
      <a-avatar :size="100" image-url="/images/tdragon6.jpg" />
    </div>
    <a-card-meta
      title="trdagon6"
      :description="$t('dashboard.author.description')"
    >
      <template #avatar>
        <div
          :style="{ display: 'flex', alignItems: 'center', color: '#1D2129' }"
        >
          <a-tag color="magenta">{{ $t('dashboard.author') }}</a-tag>
        </div>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup lang="ts">
  import { visitUrl } from '@/utils/func';
</script>

<style scoped>
  :deep(.arco-card-meta-title) {
    margin-bottom: 10px;
  }
</style>
