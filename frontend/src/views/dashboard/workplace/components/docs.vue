<template>
  <a-card
    class="general-card"
    :title="$t('dashboard.docs')"
    :header-style="{ paddingBottom: '0' }"
    :body-style="{ padding: '15px 20px 13px 20px' }"
  >
    <a-space direction="vertical">
      <div class="item">
        <a-space size="large">
          <a-tag color="arcoblue" size="small">
            <template #icon>
              <icon-github />
            </template>
            {{ $t('dashboard.docs.repoUrl') }}
          </a-tag>
          <span
            class="item-content"
            @click="visitUrl('https://github.com/tdragon6/AgBox')"
          >
            <icon-link />
            {{ $t('dashboard.docs.repoUrl') }}
          </span>
        </a-space>
      </div>
      <div class="item">
        <a-space size="large">
          <a-tag color="orangered" size="small">
            <template #icon>
              <icon-home />
            </template>
            {{ $t('robots.market') }}
          </a-tag>
          <span
            class="item-content"
            @click="visitUrl('https://github.com/tdragon6/AgBox-Market')"
          >
            <icon-link />
            {{ $t('robots.market') }}
          </span>
        </a-space>
      </div>
      <div class="item">
        <a-space size="large">
          <a-tag color="magenta" size="small">
            <template #icon>
              <icon-info-circle />
            </template>
            {{ $t('dashboard.docs') }}
          </a-tag>
          <span
            class="item-content"
            @click="visitUrl('https://tdragon6.github.io/AgBox-Docs')"
          >
            <icon-link />
            {{ $t('dashboard.docs') }}
          </span>
        </a-space>
      </div>
    </a-space>
  </a-card>
</template>

<script setup lang="ts">
  import { visitUrl } from '@/utils/func';
</script>

<style scoped lang="less">
  .item {
    display: flex;
    align-items: center;
    width: 100%;
    height: 24px;
    margin-bottom: 4px;
    .item-content {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-left: 4px;
      color: var(--color-text-2);
      text-decoration: none;
      font-size: 13px;
      cursor: pointer;
    }
  }
</style>
