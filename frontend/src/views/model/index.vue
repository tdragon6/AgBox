<template>
  <div class="container">
    <Breadcrumb :items="['menu.model']" />
    <ModelCard />
  </div>
</template>

<script setup lang="ts">
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import ModelCard from './components/model-card.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
