<template>
  <div class="container">
    <Breadcrumb :items="['menu.dashboard', 'menu.dashboard.tasks']" />
    <a-card style="height: 88vh">
      <TasksTable :robot="''" :selected-session-item="{}" scope="dashboard" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
  import TasksTable from '@/views/tasks/components/tasks-table.vue';
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
