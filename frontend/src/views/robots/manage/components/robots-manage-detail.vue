<template>
  <a-card :bordered="false" :loading="editRobotsManageDetailLoading">
    <template #actions>
      <a-button
        v-debounce
        :loading="editRobotsManageDetailLoading"
        type="primary"
        :disabled="
          robotsManageEditFormModel.name === '' ||
          robotsManageEditFormModel.description === '' ||
          robotsManageEditFormModel.department === '' ||
          robotsManageEditFormModel.reasoningEffort === '' ||
          robotsManageEditFormModel.maxTurns === undefined ||
          (selectedModelConfig === '' &&
            Object.keys(props.selectedRobotsManageItem).length === 0)
        "
        @click="editRobotsManageInfo"
      >
        <a-space>
          <icon-plus
            v-if="Object.keys(props.selectedRobotsManageItem).length === 0"
          />
          <icon-save v-else />
          <span v-if="Object.keys(props.selectedRobotsManageItem).length === 0">
            {{ $t('common.create') }}
          </span>
          <span v-else>
            {{ $t('common.save') }}
          </span>
        </a-space>
      </a-button>
    </template>
    <a-row :gutter="64">
      <a-col :span="16">
        <a-form
          :model="robotsManageEditFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item field="name" :label="$t('robots.name')" required>
                <a-input
                  v-model="robotsManageEditFormModel.name"
                  :placeholder="$t('robots.name.placeholder')"
                  allow-clear
                  @keyup.enter="editRobotsManageInfo"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="reasoningEffort"
                :label="$t('robots.reasoningEffort')"
                required
              >
                <a-select
                  v-model="robotsManageEditFormModel.reasoningEffort"
                  :placeholder="$t('robots.reasoningEffort.placeholder')"
                  allow-clear
                >
                  <template #label>
                    <a-tag
                      :color="
                        robotsReasoningEffortColor[
                          robotsManageEditFormModel.reasoningEffort
                        ]
                      "
                    >
                      {{ robotsManageEditFormModel.reasoningEffort }}
                    </a-tag>
                  </template>
                  <a-option
                    v-for="item in robotsReasoningEffortOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{
                      color: robotsReasoningEffortColor[item.value],
                    }"
                  >
                    <a-tag :color="robotsReasoningEffortColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="department"
                :label="$t('robots.department')"
                required
              >
                <a-input
                  v-model="robotsManageEditFormModel.department"
                  :placeholder="$t('robots.department.placeholder')"
                  allow-clear
                  @keyup.enter="editRobotsManageInfo"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="maxTurns"
                :label="$t('robots.maxTurns')"
                required
              >
                <a-input-number
                  v-model="robotsManageEditFormModel.maxTurns"
                  :placeholder="$t('robots.maxTurns.placeholder')"
                  allow-clear
                  @keyup.enter="editRobotsManageInfo"
                />
              </a-form-item>
            </a-col>
            <a-col :span="24">
              <a-form-item
                field="description"
                :label="$t('robots.description')"
                required
              >
                <a-textarea
                  v-model="robotsManageEditFormModel.description"
                  :auto-size="{ minRows: 8, maxRows: 8 }"
                  allow-clear
                  :placeholder="$t('robots.description.placeholder')"
                />
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-col>
      <a-col :span="8">
        <a-space direction="vertical">
          <a-form-item
            :required="Object.keys(props.selectedRobotsManageItem).length === 0"
          >
            <ModelConfigSelect
              v-model:selected-model-config="selectedModelConfig"
            />
          </a-form-item>
          <a-spin :loading="modelDetailLoading" style="display: flex">
            <ModelConfigDetail
              v-if="Object.keys(modelDetail).length !== 0"
              :model-detail="modelDetail"
            />
            <Empty v-else />
          </a-spin>
        </a-space>
      </a-col>
    </a-row>
    <a-divider />
  </a-card>
</template>

<script setup lang="ts">
  import { ref, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import { robotsReasoningEffortColor } from '@/utils/func';
  import {
    apiCreateRobotsManage,
    apiUpdateRobotsManage,
    apiGetRobotsManageModelDetail,
  } from '@/api/robots/manage';
  import { apiGetModelDetail } from '@/api/model';
  import ModelConfigSelect from '@/components/model/model-config-select/index.vue';
  import ModelConfigDetail from '@/components/model/model-config-detail/index.vue';
  import Empty from '@/components/empty/index.vue';

  const { t } = useI18n();

  const props = defineProps<{
    selectedRobotsManageItem: Record<string, any>;
  }>();
  const emit = defineEmits<{ close: []; refresh: [] }>();

  const modelDetailLoading = ref(false);
  const editRobotsManageDetailLoading = ref(false);

  const selectedModelConfig = ref('');
  const modelDetail = ref<Record<string, any>>({});

  const robotsReasoningEffortOptions = ref([
    {
      value: 'none',
      label: 'none',
    },
    {
      value: 'minimal',
      label: 'minimal',
    },
    {
      value: 'low',
      label: 'low',
    },
    {
      value: 'medium',
      label: 'medium',
    },
    {
      value: 'high',
      label: 'high',
    },
    {
      value: 'xhigh',
      label: 'xhigh',
    },
  ]);

  const robotsManageEditFormModel = ref({
    name:
      props.selectedRobotsManageItem.name !== undefined
        ? props.selectedRobotsManageItem.name
        : '',
    description:
      props.selectedRobotsManageItem.description !== undefined
        ? props.selectedRobotsManageItem.description
        : '',
    department:
      props.selectedRobotsManageItem.department !== undefined
        ? props.selectedRobotsManageItem.department
        : '',
    modelConfig:
      props.selectedRobotsManageItem.model_config_id !== undefined
        ? props.selectedRobotsManageItem.model_config_id
        : '',
    reasoningEffort:
      props.selectedRobotsManageItem.reasoning_effort !== undefined
        ? props.selectedRobotsManageItem.reasoning_effort
        : 'medium',
    maxTurns:
      props.selectedRobotsManageItem.max_turns !== undefined
        ? props.selectedRobotsManageItem.max_turns
        : 900,
  });

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

  // 获取数字员工模型配置详情
  const getRobotsManageModelDetail = async () => {
    modelDetailLoading.value = true;
    try {
      const { data } = await apiGetRobotsManageModelDetail({
        name: props.selectedRobotsManageItem.name,
        coordinator: false,
      });
      modelDetail.value = data;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelDetailLoading.value = false;
    }
  };

  // 获取编辑数字员工信息请求参数
  const getRobotsManageEditRequestParams = () => {
    const name = robotsManageEditFormModel.value.name.trim();
    const description = robotsManageEditFormModel.value.description.trim();
    const department = robotsManageEditFormModel.value.department.trim();
    const { reasoningEffort, maxTurns } = robotsManageEditFormModel.value;

    const params: Record<string, any> = {
      description,
      department,
      reasoning_effort: reasoningEffort,
      max_turns: maxTurns,
    };

    if (Object.keys(props.selectedRobotsManageItem).length === 0) {
      params.name = name;
      params.model_config_id = selectedModelConfig.value;
    } else {
      params.name = props.selectedRobotsManageItem.name;
      params.rename = name;
      if (selectedModelConfig.value !== '') {
        params.model_config_id = selectedModelConfig.value;
      }
    }

    return params;
  };

  // 编辑数字员工信息
  const editRobotsManageInfo = async () => {
    editRobotsManageDetailLoading.value = true;
    try {
      const params = getRobotsManageEditRequestParams();

      if (Object.keys(props.selectedRobotsManageItem).length === 0) {
        await apiCreateRobotsManage(params);
      } else {
        await apiUpdateRobotsManage(params);
      }

      emit('refresh');
      if (Object.keys(props.selectedRobotsManageItem).length === 0) {
        emit('close');
        Message.success(t('common.create.success'));
      } else {
        Message.success(t('common.save.success'));
      }
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      editRobotsManageDetailLoading.value = false;
    }
  };

  onMounted(() => {
    if (Object.keys(props.selectedRobotsManageItem).length !== 0) {
      getRobotsManageModelDetail();
    }
  });

  watch(
    () => selectedModelConfig.value,
    () => {
      getModelDetail();
    }
  );
</script>
