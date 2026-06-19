<template>
  <div class="container">
    <Breadcrumb :items="['menu.tasks', 'menu.tasks.project']" />
    <div class="layout">
      <div class="layout-left-side" :resize-directions="['right']">
        <ProjectItems v-model:selected-project-item="selectedProjectItem" />
      </div>
      <div class="layout-content">
        <div class="container">
          <a-card style="height: 88vh">
            <template #title>
              <RobotsSelect
                v-model:selected-robot="selectedRobot"
                style="width: 15%"
                :multiple="false"
                :selected-project-item="selectedProjectItem"
                scope="project"
              />
            </template>
            <template #extra>
              <a-tooltip
                v-if="Object.keys(selectedProjectItem).length !== 0"
                :content="$t('tasks.workspaces')"
              >
                <icon-folder
                  v-debounce
                  class="custom-icon-button"
                  @click="openWorkspaces = true"
                />
              </a-tooltip>
            </template>
            <a-tabs v-model:active-key="tasksTabKey" style="margin-left: 10px">
              <a-tab-pane key="tasks" :title="$t('tasks')">
                <TasksTable
                  v-if="
                    selectedRobot !== '' &&
                    Object.keys(selectedProjectItem).length !== 0 &&
                    tasksTabKey === 'tasks'
                  "
                  :robot="selectedRobot"
                  :selected-session-item="selectedProjectItem"
                  scope="project"
                />
                <Empty v-else />
              </a-tab-pane>
              <a-tab-pane key="messages" :title="$t('tasks.message')">
                <TasksMessages
                  v-if="
                    selectedRobot !== '' &&
                    Object.keys(selectedProjectItem).length !== 0 &&
                    tasksTabKey === 'messages'
                  "
                  :selected-tasks-or-session-item="selectedProjectItem"
                  :robot="selectedRobot"
                />
                <Empty v-else />
              </a-tab-pane>
              <a-tab-pane key="cost" :title="$t('model.cost')">
                <a-spin :spinning="projectModelCostloading" style="width: 100%">
                  <ModelCost
                    v-if="
                      Object.keys(projectCostItem).length !== 0 &&
                      tasksTabKey === 'cost'
                    "
                    :included-model-cost-item="projectCostItem"
                  />
                  <Empty v-else />
                </a-spin>
              </a-tab-pane>
            </a-tabs>
          </a-card>
        </div>
      </div>
    </div>
  </div>
  <Files
    v-if="openWorkspaces === true"
    :name="selectedProjectItem.id"
    scope="workspaces"
    :robot="''"
    @close="openWorkspaces = false"
  />
</template>

<script setup lang="ts">
  import { ref, watch, onMounted } from 'vue';
  import Files from '@/components/files/index.vue';
  import Empty from '@/components/empty/index.vue';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';
  import { apiGetRobotsSessions } from '@/api/tasks/session';
  import ModelCost from '@/components/model/model-cost/index.vue';
  import { ModelCostKeysMap } from '@/utils/func';
  import NProgress from 'nprogress';
  import ProjectItems from './components/project-items.vue';
  import TasksTable from '../components/tasks-table.vue';
  import TasksMessages from '../components/tasks-messages.vue';

  const projectModelCostloading = ref(false);

  const openWorkspaces = ref(false);
  const selectedRobot = ref('');
  const selectedProjectItem = ref<Record<string, any>>({});
  const tasksTabKey = ref('tasks');
  const projectCostItem = ref<Record<string, any>>({});

  // 获取指定项目指定数字员工模型消耗
  const getProjectCostItem = async () => {
    projectModelCostloading.value = true;
    try {
      if (selectedRobot.value === '') {
        return;
      }
      projectCostItem.value = {};
      const { data } = await apiGetRobotsSessions({
        name: selectedRobot.value.startsWith('#')
          ? selectedRobot.value.slice(1)
          : selectedRobot.value,
        coordinator: selectedRobot.value.startsWith('#'),
        ignore_coordinator_filter: true,
      });
      const nowRobotItem = data.find(
        (item: Record<string, any>) => item.id === selectedProjectItem.value.id
      );

      if (nowRobotItem !== undefined) {
        Object.keys(ModelCostKeysMap).forEach((key) => {
          projectCostItem.value[key] = nowRobotItem[ModelCostKeysMap[key]];
        });
      }
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectModelCostloading.value = false;
    }
  };

  onMounted(() => {
    NProgress.done();
  });

  watch(
    () => selectedRobot.value,
    () => getProjectCostItem()
  );

  watch(
    () => selectedProjectItem.value.id,
    () => getProjectCostItem()
  );
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }

  .layout {
    display: flex;

    &-left-side {
      flex-basis: 35vh;
      overflow: hidden;
    }

    &-content {
      flex: 1;
      margin: 0 -10px;
    }

    &-right-side {
      flex-basis: 280px;
    }
  }
</style>

<style scoped lang="less">
  @media (max-width: @screen-lg) {
    .layout {
      flex-wrap: wrap;

      &-left-side {
        flex: 1;
        flex-basis: 100%;
        margin-bottom: 16px;
      }

      &-content {
        flex: none;
        flex-basis: 100%;
        order: -1;
        margin-bottom: 16px;
        padding: 0;
      }
    }
  }
</style>
