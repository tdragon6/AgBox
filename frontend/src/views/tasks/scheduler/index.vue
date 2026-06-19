<template>
  <div class="container">
    <Breadcrumb :items="['menu.tasks', 'menu.tasks.scheduler']" />
    <SchedulerTable />
  </div>
</template>

<script setup lang="ts">
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import SchedulerTable from './components/scheduler-table.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
