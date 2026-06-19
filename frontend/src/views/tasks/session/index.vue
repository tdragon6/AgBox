<template>
  <div class="container">
    <Breadcrumb :items="['menu.tasks', 'menu.tasks.session']" />
    <div class="layout">
      <div class="layout-left-side" :resize-directions="['right']">
        <SessionItems
          v-model:selected-session-item="selectedSessionItem"
          v-model:selected-robot="selectedRobot"
        />
      </div>
      <div class="layout-content">
        <div class="container">
          <a-card style="height: 88vh">
            <template #title>
              <a-space v-if="selectedRobot !== ''">
                <Media
                  :style="{
                    marginRight: '3px',
                    backgroundColor: '#ffffff',
                  }"
                  :size="25"
                  :url="apiGetRobotsManageAvatarUrl({ name: selectedRobot })"
                  scope="avatar"
                />
                {{ selectedRobot }}
              </a-space>
            </template>
            <template #extra>
              <a-tooltip
                v-if="Object.keys(selectedSessionItem).length !== 0"
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
                    Object.keys(selectedSessionItem).length !== 0 &&
                    tasksTabKey === 'tasks'
                  "
                  :robot="selectedRobot"
                  :selected-session-item="selectedSessionItem"
                  scope="session"
                />
                <Empty v-else />
              </a-tab-pane>
              <a-tab-pane key="messages" :title="$t('tasks.message')">
                <TasksMessages
                  v-if="
                    selectedRobot !== '' &&
                    Object.keys(selectedSessionItem).length !== 0 &&
                    tasksTabKey === 'messages'
                  "
                  :selected-tasks-or-session-item="selectedSessionItem"
                  :robot="selectedRobot"
                />
                <Empty v-else />
              </a-tab-pane>
              <a-tab-pane key="cost" :title="$t('model.cost')">
                <ModelCost
                  v-if="
                    Object.keys(selectedSessionItem).length !== 0 &&
                    tasksTabKey === 'cost'
                  "
                  :included-model-cost-item="selectedSessionItem"
                />
                <Empty v-else />
              </a-tab-pane>
            </a-tabs>
          </a-card>
        </div>
      </div>
    </div>
  </div>
  <Files
    v-if="openWorkspaces === true"
    :name="selectedSessionItem.id"
    scope="workspaces"
    :robot="''"
    @close="openWorkspaces = false"
  />
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import Files from '@/components/files/index.vue';
  import Empty from '@/components/empty/index.vue';
  import Media from '@/components/media/index.vue';
  import ModelCost from '@/components/model/model-cost/index.vue';
  import NProgress from 'nprogress';
  import SessionItems from './components/session-items.vue';
  import TasksTable from '../components/tasks-table.vue';
  import TasksMessages from '../components/tasks-messages.vue';

  const openWorkspaces = ref(false);
  const selectedRobot = ref('');
  const selectedSessionItem = ref<Record<string, any>>({});
  const tasksTabKey = ref('tasks');

  onMounted(() => {
    NProgress.done();
  });
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
