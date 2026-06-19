<template>
  <a-card :title="$t('tasks.coordinator')">
    <template #extra>
      <a-button
        v-debounce
        type="primary"
        size="small"
        :loading="modelDetailLoading"
        @click="saveCoordinatorModelDetail"
      >
        {{ $t('common.save') }}
      </a-button>
    </template>
    <a-space direction="vertical" size="large">
      <a-space size="large">
        <a-radio-group v-model="selectedCoordinator" type="button">
          <a-radio value="agbox-coordinator-sync">
            {{ $t(coordinatorName['agbox-coordinator-sync']) }}
          </a-radio>
          <a-radio value="agbox-coordinator-async">
            {{ $t(coordinatorName['agbox-coordinator-async']) }}
          </a-radio>
        </a-radio-group>
        <ModelConfigSelect
          v-model:selected-model-config="selectedModelConfig"
        />
      </a-space>
      <a-spin :loading="modelDetailLoading" style="display: flex">
        <ModelConfigDetail
          v-if="Object.keys(modelDetail).length !== 0"
          :model-detail="modelDetail"
        />
        <Empty v-else />
      </a-spin>
    </a-space>
  </a-card>
</template>

<script setup lang="ts">
  import { ref, watch, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import {
    apiGetRobotsManageModelDetail,
    apiSaveRobotsManageModelDetail,
  } from '@/api/robots/manage';
  import { apiGetModelDetail } from '@/api/model';
  import ModelConfigSelect from '@/components/model/model-config-select/index.vue';
  import ModelConfigDetail from '@/components/model/model-config-detail/index.vue';
  import { coordinatorName } from '@/utils/func';
  import Empty from '@/components/empty/index.vue';

  const { t } = useI18n();

  const modelDetailLoading = ref(false);

  const selectedCoordinator = ref('agbox-coordinator-sync');
  const selectedModelConfig = ref('');
  const modelDetail = ref<Record<string, any>>({});

  // 获取模型配置详情
  const getModelDetail = async () => {
    modelDetailLoading.value = true;
    if (selectedModelConfig.value === '') {
      modelDetail.value = {};
    } else {
      const { data } = await apiGetModelDetail({
        id: selectedModelConfig.value,
      });
      modelDetail.value = data;
    }
    modelDetailLoading.value = false;
  };

  // 获取协调器模型配置详情
  const getCoordinatorModelDetail = async () => {
    modelDetailLoading.value = true;
    try {
      const { data } = await apiGetRobotsManageModelDetail({
        name: selectedCoordinator.value,
        coordinator: true,
      });
      modelDetail.value = data;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelDetailLoading.value = false;
    }
  };

  // 保存协调器模型配置
  const saveCoordinatorModelDetail = async () => {
    modelDetailLoading.value = true;
    try {
      await apiSaveRobotsManageModelDetail({
        name: selectedCoordinator.value,
        model_config_id: selectedModelConfig.value,
        coordinator: true,
      });
      getCoordinatorModelDetail();
      Message.success(t('common.save.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelDetailLoading.value = false;
    }
  };

  onMounted(() => {
    getCoordinatorModelDetail();
  });

  watch(
    () => selectedModelConfig.value,
    () => {
      getModelDetail();
    }
  );

  watch(
    () => selectedCoordinator.value,
    () => {
      getCoordinatorModelDetail();
    }
  );
</script>
