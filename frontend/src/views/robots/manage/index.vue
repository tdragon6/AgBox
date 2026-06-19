<template>
  <div class="container">
    <Breadcrumb :items="['menu.robots', 'menu.robots.manage']" />
    <RobotsManageTable />
  </div>
</template>

<script setup lang="ts">
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import RobotsManageTable from './components/robots-manage-table.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
