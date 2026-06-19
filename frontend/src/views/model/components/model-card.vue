<template>
  <a-card :bordered="false" :loading="modelItemsLoading">
    <template #title>
      <a-space size="medium">
        {{ $t('model') }}
        <a-radio-group
          v-model="isOnlineOptions"
          type="button"
          size="small"
          @change="getModelItems"
        >
          <a-radio value="all">
            <a-badge color="arcoblue" :text="$t('common.all')"></a-badge>
          </a-radio>
          <a-radio value="online">
            <a-badge status="success" :text="$t('common.online')"></a-badge>
          </a-radio>
          <a-radio value="offline">
            <a-badge status="normal" :text="$t('common.offline')"></a-badge>
          </a-radio>
        </a-radio-group>
      </a-space>
    </template>
    <template #extra>
      <a-input
        v-model="modelSearchKeyword"
        :placeholder="$t('common.keyword.placeholder')"
        allow-clear
        @keyup.enter="getModelItems"
      >
        <template #suffix>
          <icon-search />
        </template>
      </a-input>
    </template>
    <a-row :gutter="[16, 16]">
      <a-col v-for="item in modelItems" :key="item.id" :span="6">
        <a-card>
          <template #title>
            <a-space :size="18">
              <a-avatar
                :style="{ backgroundColor: 'var(--color-bg-2)' }"
                :image-url="`/images/provider/${
                  item.provider_id.split('-')[0]
                }.svg`"
              />
              <a-space direction="vertical" size="mini">
                <span style="font-size: 20px">{{ item.name }}</span>
                <a-tag color="arcoblue" bordered size="small">
                  <template #icon> <icon-at /> </template>
                  {{ item.provider_name }}
                </a-tag>
              </a-space>
            </a-space>
          </template>
          <template #extra>
            <a-badge
              :status="item.is_online ? 'success' : 'normal'"
              :text="
                item.is_online ? $t('common.online') : $t('common.offline')
              "
            />
          </template>
          <a-tag color="magenta" bordered size="small">
            <template #icon> <icon-robot /> </template>
            {{ item.model }}
          </a-tag>
          <a-divider type="dashed" />
          <template #actions>
            <a-button
              v-debounce
              type="outline"
              size="mini"
              @click="openEditModelModal(item)"
            >
              <a-space>
                <icon-edit />
                {{ $t('common.edit') }}
              </a-space>
            </a-button>
            <a-popconfirm
              type="warning"
              :content="$t('common.confirm.delete')"
              @ok="deleteModel(item.id)"
              @ok-loading="modelItemsLoading"
            >
              <a-button type="outline" status="danger" size="mini">
                <a-space>
                  <icon-delete />
                  {{ $t('common.delete') }}
                </a-space>
              </a-button>
            </a-popconfirm>
          </template>
          <a-card-meta>
            <template #avatar>
              {{ dayjs(item.updated_time).format('YYYY-MM-DD HH:mm:ss') }}
            </template>
          </a-card-meta>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card
          v-debounce
          hoverable
          style="cursor: pointer; min-height: 194px"
          @click="modelDetail.name = 'default'"
        >
          <a-result :status="null">
            <template #title>
              <a-typography-text type="secondary">
                {{ $t('common.create') }}
              </a-typography-text>
            </template>
            <template #icon>
              <icon-plus style="font-size: 32px" />
            </template>
          </a-result>
        </a-card>
      </a-col>
    </a-row>
  </a-card>
  <ModelEdit
    v-if="Object.keys(modelDetail).length !== 0"
    :model-detail="modelDetail"
    @close="modelDetail = {}"
    @refresh="getModelItems"
  />
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import { apiGetModelItems, apiDeleteModel } from '@/api/model';
  import ModelEdit from '@/components/model/model-edit/index.vue';

  const { t } = useI18n();

  const modelItemsLoading = ref(false);

  const isOnlineOptions = ref<'all' | 'online' | 'offline'>('all');
  const modelSearchKeyword = ref('');
  const modelItems = ref<Record<string, any>[]>([]);
  const modelDetail = ref<Record<string, any>>({});

  // 获取模型配置列表
  const getModelItems = async () => {
    modelItemsLoading.value = true;
    try {
      const params: Record<string, any> = {
        keyword: modelSearchKeyword.value,
      };

      if (
        isOnlineOptions.value === 'online' ||
        isOnlineOptions.value === 'offline'
      ) {
        params.is_online = isOnlineOptions.value === 'online';
      }

      const { data } = await apiGetModelItems(params);
      modelItems.value = data;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelItemsLoading.value = false;
    }
  };

  // 打开编辑模型配置弹窗
  const openEditModelModal = (item: Record<string, any>) => {
    modelDetail.value.id = item.id;
    modelDetail.value.name = item.name;
    modelDetail.value.providerID = item.provider_id;
    modelDetail.value.providerName = item.provider_name;
    modelDetail.value.baseUrl = item.base_url;
    modelDetail.value.apiKey = item.api_key;
    modelDetail.value.model = item.model;
    modelDetail.value.isOnline = item.is_online;
    modelDetail.value.updatedTime = item.updated_time;
  };

  // 删除模型配置
  const deleteModel = async (id: string) => {
    modelItemsLoading.value = true;
    try {
      await apiDeleteModel({
        ids: [id],
      });
      await getModelItems();
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      modelItemsLoading.value = false;
    }
  };

  onMounted(() => {
    getModelItems();
  });
</script>

<style scoped lang="less">
  :deep(.arco-card-header) {
    height: auto;
    border: none;
  }
</style>
