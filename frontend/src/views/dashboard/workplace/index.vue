<template>
  <div class="container">
    <div class="left-side">
      <div class="panel">
        <Banner />
        <DataPanel />
      </div>
      <a-grid :cols="24" :col-gap="16" :row-gap="16" style="margin-top: 16px">
        <a-grid-item
          :span="{ xs: 24, sm: 24, md: 24, lg: 12, xl: 12, xxl: 12 }"
        >
          <a-card :title="$t('model.cost')">
            <a-tabs
              v-model:active-key="modelCostTabKey"
              @change="
                modelCostTabKey === 'all'
                  ? getAllModelCostItem()
                  : getRobotsCostItem()
              "
            >
              <a-tab-pane key="all">
                <template #title>
                  {{ $t('common.all') }}
                </template>
                <ModelCost
                  v-if="modelCostTabKey === 'all'"
                  :included-model-cost-item="allModelCostItem"
                />
              </a-tab-pane>
              <a-tab-pane key="robots">
                <template #title>
                  {{ $t('robots') }}
                </template>
                <a-space
                  v-if="modelCostTabKey === 'robots'"
                  direction="vertical"
                  style="width: 100%"
                  size="medium"
                >
                  <RobotsSelect
                    v-model:selected-robot="selectedRobot"
                    style="width: 30%"
                    :multiple="false"
                    :selected-project-item="{ robots: robotsNames }"
                    :scope="'project'"
                  />
                  <a-spin
                    :spinning="robotsModelCostloading"
                    style="width: 100%"
                  >
                    <ModelCost :included-model-cost-item="robotsCostItem" />
                  </a-spin>
                </a-space>
              </a-tab-pane>
            </a-tabs>
          </a-card>
        </a-grid-item>
        <a-grid-item
          :span="{ xs: 24, sm: 24, md: 24, lg: 12, xl: 12, xxl: 12 }"
        >
          <SystemInfo />
        </a-grid-item>
      </a-grid>
    </div>
    <div class="right-side">
      <a-grid :cols="24" :row-gap="16">
        <a-grid-item class="panel" :span="24">
          <Author />
        </a-grid-item>
        <a-grid-item class="panel" :span="24">
          <a-image src="/images/dashboard/perfect_loop.gif" width="280" />
        </a-grid-item>
        <a-grid-item class="panel" :span="24">
          <Docs />
        </a-grid-item>
      </a-grid>
    </div>
  </div>
  <a-modal
    v-model:visible="hintModelConfigModalVisible"
    :title="$t('model')"
    @ok="modelEditModalVisible = true"
  >
    {{ $t('dashboard.model.hint') }}
  </a-modal>
  <ModelEdit
    v-if="modelEditModalVisible === true"
    :model-detail="{name: 'default'}"
    @close="modelEditModalVisible = false"
  />
</template>

<script setup lang="ts">
  import { ref, onMounted, watch } from 'vue';
  import { apiGetRobotsManageItems } from '@/api/robots/manage';
  import { apiGetRobotsSessions } from '@/api/tasks/session';
  import { apiGetModelItems } from '@/api/model';
  import ModelCost from '@/components/model/model-cost/index.vue';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';
  import { ModelCostKeysMap } from '@/utils/func';
  import ModelEdit from '@/components/model/model-edit/index.vue';
  import NProgress from 'nprogress';
  import Banner from './components/banner.vue';
  import DataPanel from './components/data-panel.vue';
  import SystemInfo from './components/system-info.vue';
  import Author from './components/author.vue';
  import Docs from './components/docs.vue';

  const robotsModelCostloading = ref(false);

  const hintModelConfigModalVisible = ref(false);
  const modelEditModalVisible = ref(false);

  const modelCostTabKey = ref('all');
  const selectedRobot = ref('');
  const robotsNames = ref<string[]>([]);
  const robotsCostItemDefault = ref<Record<string, any>>({
    inputTokens: 0,
    outputTokens: 0,
    cacheReadTokens: 0,
    cacheWriteTokens: 0,
    reasoningTokens: 0,
    estimatedCostUsd: 0,
    actualCostUsd: 0,
  });
  const allModelCostItem = ref<Record<string, any>>(
    robotsCostItemDefault.value
  );
  const robotsCostItem = ref<Record<string, any>>(robotsCostItemDefault.value);

  const getRobotsNames = async () => {
    try {
      const { data } = await apiGetRobotsManageItems({ page: 0 });
      robotsNames.value = [];
      data.items.forEach((item: Record<string, any>) => {
        robotsNames.value.push(item.name);
      });
    } catch (_) {
      /* eslint-disable no-empty */
    }
  };

  // 获取指定数字员工模型消耗
  const getRobotsCostItem = async () => {
    robotsModelCostloading.value = true;
    try {
      if (selectedRobot.value === '') {
        return;
      }

      robotsCostItem.value = { ...robotsCostItemDefault.value };

      const { data } = await apiGetRobotsSessions({
        name: selectedRobot.value.startsWith('#')
          ? selectedRobot.value.slice(1)
          : selectedRobot.value,
        coordinator: selectedRobot.value.startsWith('#'),
        ignore_coordinator_filter: true,
      });

      data.forEach((item: Record<string, any>) => {
        Object.keys(ModelCostKeysMap).forEach((key) => {
          robotsCostItem.value[key] += item[ModelCostKeysMap[key]];
        });
      });
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsModelCostloading.value = false;
    }
  };

  // 获取所有数字员工模型消耗
  const getAllModelCostItem = async () => {
    try {
      const promises: Promise<any>[] = [];
      [
        ...robotsNames.value,
        '#agbox-coordinator-sync',
        '#agbox-coordinator-async',
      ].forEach((robot) => {
        promises.push(
          apiGetRobotsSessions({
            name: robot.startsWith('#') ? robot.slice(1) : robot,
            coordinator: robot.startsWith('#'),
            ignore_coordinator_filter: true,
          })
        );
      });
      const responses = await Promise.all(promises);
      allModelCostItem.value = { ...robotsCostItemDefault.value };
      responses.forEach((response) => {
        response.data.forEach((item: Record<string, any>) => {
          Object.keys(ModelCostKeysMap).forEach((key) => {
            allModelCostItem.value[key] += item[ModelCostKeysMap[key]];
          });
        });
      });
    } catch (_) {
      /* eslint-disable no-empty */
    }
  };

  const initHintModelConfig = async () => {
    try {
      const { data } = await apiGetModelItems({});
      if (data.length === 0) {
        hintModelConfigModalVisible.value = true;
      }
    } catch (_) {
      /* eslint-disable no-empty */
    }
  };

  onMounted(() => {
    NProgress.done();
    getRobotsNames();
    getAllModelCostItem();
    initHintModelConfig();
  });

  watch(
    () => selectedRobot.value,
    () => getRobotsCostItem()
  );
</script>

<style lang="less" scoped>
  .container {
    background-color: var(--color-fill-2);
    padding: 16px 20px;
    padding-bottom: 0;
    display: flex;
  }

  .left-side {
    flex: 1;
    overflow: auto;
  }

  .right-side {
    width: 280px;
    margin-left: 16px;
  }

  .panel {
    background-color: var(--color-bg-2);
    border-radius: 4px;
    overflow: auto;
  }
  :deep(.panel-border) {
    margin-bottom: 0;
    border-bottom: 1px solid rgb(var(--gray-2));
  }
</style>

<style lang="less" scoped>
  .mobile {
    .container {
      display: block;
    }
    .right-side {
      // display: none;
      width: 100%;
      margin-left: 0;
      margin-top: 16px;
    }
  }
</style>
