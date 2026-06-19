<template>
  <a-space :size="10">
    {{ $t('model') }}
    <a-select
      v-model="selectedModelConfig"
      v-debounce
      :loading="modelConfigLoading"
      :placeholder="$t('model.config.placeholder')"
      allow-search
      allow-clear
      style="width: 35vh"
      @click="getModelConfig()"
    >
      <template #label>
        <a-space :size="18">
          <a-avatar
            :size="20"
            :style="{ backgroundColor: 'var(--color-bg-2)' }"
            :image-url="`/images/provider/${
              modelConfigOptions
                .find((item) => item.id === selectedModelConfig)
                ?.provider_id.split('-')[0]
            }.svg`"
          />
          <a-typography-text bold style="font-size: 15px">
            {{
              modelConfigOptions.find((item) => item.id === selectedModelConfig)
                ?.name
            }}
          </a-typography-text>
          <a-typography-text type="secondary" style="font-size: 12px">
            {{
              modelConfigOptions.find((item) => item.id === selectedModelConfig)
                ?.model
            }}
          </a-typography-text>
        </a-space>
      </template>
      <a-option
        v-for="item in modelConfigOptions"
        :key="item.id"
        :value="item.id"
      >
        <a-space :size="18">
          <a-avatar
            :size="25"
            :style="{ backgroundColor: 'var(--color-bg-2)' }"
            :image-url="`/images/provider/${
              item.provider_id.split('-')[0]
            }.svg`"
          />
          <a-space :size="0" direction="vertical">
            <a-typography-text bold style="font-size: 15px">
              {{ item.name }}
            </a-typography-text>
            <a-typography-text type="secondary" style="font-size: 12px">
              {{ item.model }}
            </a-typography-text>
          </a-space>
        </a-space>
      </a-option>
    </a-select>
  </a-space>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { apiGetModelItems } from '@/api/model';

  const modelConfigLoading = ref(false);

  const modelConfigOptions = ref<Record<string, any>[]>([]);

  const selectedModelConfig = defineModel<string>('selectedModelConfig');

  // 获取模型配置列表
  const getModelConfig = async () => {
    modelConfigLoading.value = true;
    try {
      const { data } = await apiGetModelItems({
        is_online: true,
      });
      modelConfigOptions.value = data;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelConfigLoading.value = false;
    }
  };
</script>
