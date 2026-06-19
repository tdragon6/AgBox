<template>
  <a-grid :cols="24" :row-gap="16" class="panel">
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="robotsTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/robots.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('robots')"
            :value="robotsTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="skillsTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/skills.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('skills')"
            :value="skillsTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="projectTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/project.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('tasks.project')"
            :value="projectTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item :span="24">
      <a-divider class="panel-border" />
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="tasksTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/tasks.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('tasks')"
            :value="tasksTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="modelTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/model.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('model')"
            :value="modelTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item
      class="panel-col"
      :span="{ xs: 12, sm: 12, md: 12, lg: 12, xl: 12, xxl: 8 }"
    >
      <a-spin :loading="schedulerTotalLoading">
        <a-space>
          <a-avatar :size="54" class="col-avatar">
            <img
              style="width: 60%; display: block; margin: auto"
              alt="avatar"
              src="/images/dashboard/scheduler.svg"
            />
          </a-avatar>
          <a-statistic
            :title="$t('tasks.scheduler')"
            :value="schedulerTotal"
            :value-from="0"
            animation
          >
          </a-statistic>
        </a-space>
      </a-spin>
    </a-grid-item>
    <a-grid-item :span="24">
      <a-divider class="panel-border" />
    </a-grid-item>
  </a-grid>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { apiGetRobotsManageItems } from '@/api/robots/manage';
  import { apiGetSkillsItems } from '@/api/skills';
  import { apiGetProjectItems } from '@/api/tasks/project';
  import { apiGetTasksItems } from '@/api/tasks/task';
  import { apiGetModelItems } from '@/api/model';
  import { apiGetSchedulerItems } from '@/api/tasks/scheduler';

  const robotsTotalLoading = ref(false);
  const skillsTotalLoading = ref(false);
  const projectTotalLoading = ref(false);
  const tasksTotalLoading = ref(false);
  const modelTotalLoading = ref(false);
  const schedulerTotalLoading = ref(false);

  const robotsTotal = ref(0);
  const skillsTotal = ref(0);
  const projectTotal = ref(0);
  const tasksTotal = ref(0);
  const modelTotal = ref(0);
  const schedulerTotal = ref(0);

  const getRobotsTotal = async () => {
    robotsTotalLoading.value = true;
    try {
      const { data } = await apiGetRobotsManageItems({
        page: 0,
      });
      robotsTotal.value = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsTotalLoading.value = false;
    }
  };

  const getSkillsTotal = async () => {
    skillsTotalLoading.value = true;
    try {
      const { data } = await apiGetSkillsItems({
        page: 0,
      });
      skillsTotal.value = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsTotalLoading.value = false;
    }
  };

  const getProjectTotal = async () => {
    projectTotalLoading.value = true;
    try {
      const { data } = await apiGetProjectItems({
        page: 0,
      });
      projectTotal.value = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectTotalLoading.value = false;
    }
  };

  const getTasksTotal = async () => {
    tasksTotalLoading.value = true;
    try {
      const { data } = await apiGetTasksItems({
        page: 0,
      });
      tasksTotal.value = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      tasksTotalLoading.value = false;
    }
  };

  const getModelTotal = async () => {
    modelTotalLoading.value = true;
    try {
      const { data } = await apiGetModelItems({});
      modelTotal.value = data.length;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelTotalLoading.value = false;
    }
  };

  const getSchedulerTotal = async () => {
    schedulerTotalLoading.value = true;
    try {
      const { data } = await apiGetSchedulerItems({});
      schedulerTotal.value = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerTotalLoading.value = false;
    }
  };

  onMounted(() => {
    getRobotsTotal();
    getSkillsTotal();
    getProjectTotal();
    getTasksTotal();
    getModelTotal();
    getSchedulerTotal();
  });
</script>

<style lang="less" scoped>
  .arco-grid.panel {
    margin-bottom: 0;
    padding: 16px 20px 0 20px;
  }
  .panel-col {
    padding-left: 30px;
    border-right: 1px solid rgb(var(--gray-2));
  }
  .col-avatar {
    margin-right: 12px;
    background-color: var(--color-fill-2);
  }
  :deep(.panel-border) {
    margin: 4px 0 0 0;
  }
</style>
