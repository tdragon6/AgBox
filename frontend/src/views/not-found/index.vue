<template>
  <div class="content">
    <a-result class="result" status="404" :subtitle="$t('notFound')">
    </a-result>
    <div class="operation-row">
      <a-button type="primary" @click="router.back()">
        {{ $t('notFound.back') }}
      </a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import NProgress from 'nprogress';

  const router = useRouter();

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .content {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -95px;
    margin-top: -121px;
    text-align: center;
  }
</style>
