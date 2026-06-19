<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    :footer="false"
    width="60%"
    :title="$t('model')"
    @cancel="emit('close')"
  >
    <div style="display: flex">
      <div class="step-aside">
        <a-steps :current="currentStep" direction="vertical">
          <a-step>{{ $t('model.name') }}</a-step>
          <a-step>{{ $t('model.provider') }}</a-step>
          <a-step>{{ $t('model.auth') }}</a-step>
          <a-step>{{ $t('model.list') }}</a-step>
        </a-steps>
      </div>
      <div style="width: 100%">
        <div v-if="currentStep === 1" class="custom-center">
          <a-space>
            <a-form-item required :label="$t('model.name')">
              <a-input
                v-model="modelName"
                style="width: 15vw"
                :placeholder="$t('model.name.placeholder')"
                allow-clear
                @keyup.enter="nextStep"
              />
            </a-form-item>
          </a-space>
        </div>
        <div v-else-if="currentStep === 2" class="custom-center">
          <a-space>
            <a-form-item required :label="$t('model.provider')">
              <a-space>
                <a-select
                  v-model="selectedModelProviderID"
                  :loading="modelProviderLoading"
                  style="width: 15vw"
                  :placeholder="$t('model.provider.placeholder')"
                  allow-search
                  allow-clear
                >
                  <template #label>
                    <a-space :size="18">
                      <a-avatar
                        :size="20"
                        :style="{ backgroundColor: 'var(--color-bg-2)' }"
                      >
                        <!-- 确保新值刷新，用 img 标签 -->
                        <img
                          :src="`/images/provider/${
                            selectedModelProviderID.split('-')[0]
                          }.svg`"
                        />
                      </a-avatar>
                      {{
                        modelProviderOptions.find(
                          (item) => item.id === selectedModelProviderID
                        )?.name
                      }}
                    </a-space>
                  </template>
                  <a-option
                    v-for="item in modelProviderOptions"
                    :key="item.id"
                    :value="item.id"
                  >
                    <a-space :size="18">
                      <a-avatar
                        :size="20"
                        :style="{ backgroundColor: 'var(--color-bg-2)' }"
                        :image-url="`/images/provider/${
                          item.id.split('-')[0]
                        }.svg`"
                      />
                      {{ item.name }}
                    </a-space>
                  </a-option>
                </a-select>
                <a-tooltip :content="$t('common.refresh')">
                  <icon-refresh
                    v-debounce
                    class="custom-icon-button"
                    @click="getModelProvider"
                  />
                </a-tooltip>
              </a-space>
            </a-form-item>
          </a-space>
        </div>
        <div v-else-if="currentStep === 3" class="custom-center">
          <a-space direction="vertical" size="medium">
            <a-form-item required :label="$t('model.baseUrl')">
              <a-space>
                <a-input
                  v-model="modelBaseUrl"
                  :loading="modelBaseUrlLoading"
                  style="width: 15vw"
                  :placeholder="$t('model.baseUrl.placeholder')"
                  allow-clear
                />
                <a-tooltip :content="$t('common.refresh')">
                  <icon-refresh
                    v-debounce
                    class="custom-icon-button"
                    @click="getModelBaseUrl"
                  />
                </a-tooltip>
              </a-space>
            </a-form-item>
            <a-form-item :label="$t('model.apiKey')" style="margin-left: 16px">
              <a-input
                v-model="modelApiKey"
                style="width: 15vw"
                :placeholder="$t('model.apiKey.placeholder')"
                allow-clear
                @keyup.enter="nextStep"
              />
            </a-form-item>
          </a-space>
        </div>
        <div v-else class="custom-center">
          <a-space>
            <a-form-item required :label="$t('model.baseUrl')">
              <a-space>
                <a-select
                  v-model="selectedModelList"
                  :loading="modelListLoading"
                  style="width: 15vw"
                  :placeholder="$t('model.list.placeholder')"
                  allow-search
                  allow-clear
                >
                  <template #label>
                    <a-space :size="18">
                      <a-avatar
                        :size="20"
                        :style="{ backgroundColor: 'var(--color-bg-2)' }"
                        :image-url="`/images/provider/${
                          selectedModelProviderID.split('-')[0]
                        }.svg`"
                      />
                      {{
                        modelListOptions.find(
                          (item) => item.id === selectedModelList
                        )?.name
                      }}
                    </a-space>
                  </template>
                  <a-option
                    v-for="item in modelListOptions"
                    :key="item.id"
                    :value="item.id"
                  >
                    <a-space :size="18">
                      <a-avatar
                        :size="20"
                        :style="{ backgroundColor: 'var(--color-bg-2)' }"
                        :image-url="`/images/provider/${
                          item.providerId.split('-')[0]
                        }.svg`"
                      />
                      {{ item.name }}
                    </a-space>
                  </a-option>
                </a-select>
                <a-tooltip :content="$t('common.refresh')">
                  <icon-refresh
                    v-debounce
                    class="custom-icon-button"
                    @click="getModelList"
                  />
                </a-tooltip>
              </a-space>
            </a-form-item>
          </a-space>
        </div>

        <div class="step-bottom">
          <a-button
            v-debounce
            :disabled="currentStep === 1"
            @click="currentStep = Math.max(1, currentStep - 1)"
          >
            <icon-left />
            {{ $t('model.step.back') }}
          </a-button>
          <a-button
            v-if="currentStep !== 4"
            v-debounce
            :disabled="
              currentStep === 4 ||
              (currentStep === 1 && !modelName?.trim()) ||
              (currentStep === 2 && !selectedModelProviderID?.trim()) ||
              (currentStep === 3 && !modelBaseUrl?.trim())
            "
            @click="nextStep"
          >
            {{ $t('model.step.next') }}
            <icon-right />
          </a-button>
          <a-button
            v-else
            v-debounce
            :loading="editModelLoading"
            type="outline"
            :disabled="currentStep === 4 && !selectedModelList?.trim()"
            @click="saveModel"
          >
            <template #icon>
              <icon-save />
            </template>
            {{ $t('common.save') }}
          </a-button>
        </div>
      </div>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import {
    apiGetModelProvider,
    apiGetModelBaseUrl,
    apiGetModelList,
    apiCreateModel,
    apiUpdateModel,
  } from '@/api/model';

  const { t } = useI18n();

  const props = defineProps<{ modelDetail: Record<string, any> }>();
  const emit = defineEmits<{ close: []; refresh: [] }>();

  const currentStep = ref(1);

  const editModelLoading = ref(false);
  const modelProviderLoading = ref(false);
  const modelBaseUrlLoading = ref(false);
  const modelListLoading = ref(false);

  const modelName = ref(props.modelDetail.name);

  const selectedModelProviderID = ref(props.modelDetail.providerID);
  const modelProviderOptions = ref<Record<string, any>[]>([]);

  const modelBaseUrl = ref(props.modelDetail.baseUrl);
  const modelApiKey = ref(props.modelDetail.apiKey);

  const selectedModelList = ref(props.modelDetail.model);
  const modelListOptions = ref<Record<string, any>[]>([]);

  // 获取模型提供商列表
  const getModelProvider = async () => {
    modelProviderLoading.value = true;
    try {
      const { data } = await apiGetModelProvider();
      modelProviderOptions.value = data;

      if (!props.modelDetail.providerID) {
        selectedModelProviderID.value = modelProviderOptions.value[0].id;
      }
    } catch (_) {
      selectedModelProviderID.value = '';
      modelProviderOptions.value = [];
    } finally {
      modelProviderLoading.value = false;
    }
  };

  // 获取模型配置 Base Url
  const getModelBaseUrl = async () => {
    modelBaseUrlLoading.value = true;
    try {
      const { data } = await apiGetModelBaseUrl({
        id: selectedModelProviderID.value,
      });

      if (!props.modelDetail.baseUrl) {
        modelBaseUrl.value = data;
      }
    } catch (_) {
      modelBaseUrl.value = '';
    } finally {
      modelBaseUrlLoading.value = false;
    }
  };

  // 获取可用模型列表
  const getModelList = async () => {
    modelListLoading.value = true;
    try {
      const { data } = await apiGetModelList({
        api_key: modelApiKey.value,
        base_url: modelBaseUrl.value,
      });

      modelListOptions.value = data.map((item: string) => ({
        id: item,
        name: item,
        providerId: selectedModelProviderID.value,
      }));

      if (!props.modelDetail.model) {
        selectedModelList.value = modelListOptions.value[0].id;
      }
    } catch (_) {
      selectedModelList.value = '';
      modelListOptions.value = [];
    } finally {
      modelListLoading.value = false;
    }
  };

  // 保存模型配置
  const saveModel = async () => {
    editModelLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: modelName.value,
        provider_id: selectedModelProviderID.value,
        model: selectedModelList.value,
        base_url: modelBaseUrl.value,
      };

      if (modelApiKey.value !== '') {
        params.api_key = modelApiKey.value;
      }

      if (!props.modelDetail.id) {
        // 创建模型配置
        await apiCreateModel(params);
        Message.success(t('common.create.success'));
      } else {
        // 更新模型配置
        params.id = props.modelDetail.id;
        await apiUpdateModel(params);
        Message.success(t('common.edit.success'));
      }
      emit('refresh');
      emit('close');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      editModelLoading.value = false;
    }
  };

  // 下一步
  const nextStep = () => {
    if (currentStep.value === 1) {
      getModelProvider();
    } else if (currentStep.value === 2) {
      getModelBaseUrl();
    } else if (currentStep.value === 3) {
      getModelList();
    }
    currentStep.value = Math.min(4, currentStep.value + 1);
  };
</script>

<style scoped lang="less">
  .step-aside {
    padding: 24px;
    height: 350px;
    border-right: 1px solid var(--color-border);
  }

  .step-bottom {
    display: flex;
    justify-content: center;

    button {
      margin: 0 20px;
    }
  }
</style>
