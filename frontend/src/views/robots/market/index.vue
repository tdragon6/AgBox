<template>
  <div class="container">
    <Breadcrumb :items="['menu.robots', 'menu.robots.market']" />
    <RobotsMarketTable />
  </div>
</template>

<script setup lang="ts">
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import RobotsMarketTable from './components/robots-market-table.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
