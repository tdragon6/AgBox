<template>
  <div class="container">
    <Breadcrumb :items="['menu.settings']" />
    <a-row :gutter="[8, 8]">
      <a-col :span="12">
        <CoordinatorSettings />
      </a-col>
      <a-col :span="12">
        <SkillsSettings />
      </a-col>
      <a-col :span="12">
        <RobotsSettings />
      </a-col>
      <a-col :span="12">
        <SchedulerSettings />
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import CoordinatorSettings from './components/coordinator-settings.vue';
  import SchedulerSettings from './components/scheduler-settings.vue';
  import RobotsSettings from './components/robots-settings.vue';
  import SkillsSettings from './components/skills-settings.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
