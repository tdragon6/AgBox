<template>
  <a-card style="height: 88vh" :title="$t('robots.market')">
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="robotsMarketSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="16">
            <a-col :span="6">
              <a-form-item field="name" :label="$t('robots.name')">
                <a-input
                  v-model="robotsMarketSearchFormModel.name"
                  :placeholder="$t('robots.name.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="department" :label="$t('robots.department')">
                <a-input
                  v-model="robotsMarketSearchFormModel.department"
                  :placeholder="$t('robots.department.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="ranks" :label="$t('robots.rank')">
                <a-select
                  v-model="robotsMarketSearchFormModel.ranks"
                  :placeholder="$t('robots.rank.placeholder')"
                  multiple
                  allow-clear
                >
                  <a-option
                    v-for="item in robotsRankOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{ color: robotsRankColor[item.value] }"
                  >
                    <a-tag :color="robotsRankColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="qualities" :label="$t('robots.quality')">
                <a-select
                  v-model="robotsMarketSearchFormModel.qualities"
                  :placeholder="$t('robots.quality.placeholder')"
                  multiple
                  allow-clear
                >
                  <a-option
                    v-for="item in robotsQualityOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{ color: robotsQualityColor[item.value] }"
                  >
                    <a-tag :color="robotsQualityColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="author" :label="$t('robots.author')">
                <a-input
                  v-model="robotsMarketSearchFormModel.author"
                  :placeholder="$t('robots.author.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="description"
                :label="$t('robots.description')"
              >
                <a-input
                  v-model="robotsMarketSearchFormModel.description"
                  :placeholder="$t('robots.description.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="createdTime"
                :label="$t('common.time.created')"
              >
                <a-range-picker
                  v-model="robotsMarketSearchFormModel.createdTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="updatedTime"
                :label="$t('common.time.updated')"
              >
                <a-range-picker
                  v-model="robotsMarketSearchFormModel.updatedTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </a-col>
      <a-divider style="height: 85px" direction="vertical" />
      <a-col :flex="'86px'" style="text-align: right">
        <a-space direction="vertical" :size="18">
          <a-button
            v-debounce
            :loading="robotsMarketTableLoading"
            type="primary"
            @click="getRobotsMarketItems"
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            :loading="robotsMarketTableLoading"
            @click="resetRobotsMarketSearchFormModel"
          >
            <template #icon>
              <icon-refresh />
            </template>
            {{ $t('common.reset') }}
          </a-button>
        </a-space>
      </a-col>
    </a-row>
    <a-divider style="margin-top: 0" />
    <a-table
      row-key="name"
      :scroll="{ y: 'calc(88vh - 300px)' }"
      :loading="robotsMarketTableLoading"
      :pagination="robotsMarketTablePagination"
      :columns="robotsMarketTableColumns"
      :data="robotsMarketItems"
      :bordered="false"
      @page-change="changeRobotsMarketTablePage"
      @page-size-change="changeRobotsMarketTablePageSize"
      @sorter-change="changeRobotsMarketTableOrder"
    >
      <template #index="{ rowIndex }">
        {{
          rowIndex +
          1 +
          (robotsMarketTablePagination.current - 1) *
            robotsMarketTablePagination.pageSize
        }}
      </template>
      <template #name="{ record }">
        <span :style="{ display: 'flex', alignItems: 'center' }">
          <a-avatar
            :style="{
              marginRight: '8px',
              backgroundColor: 'var(--color-bg-2)',
              cursor: 'pointer',
            }"
            :size="35"
          >
            <img :src="`${record.avatar_url}?_t=${Date.now()}`" />
          </a-avatar>
          {{ record.name }}
        </span>
      </template>
      <template #author="{ record }">
        <a-tag color="arcoblue" bordered>
          {{ record.author }}
        </a-tag>
      </template>
      <template #rank="{ record }">
        <a-tag :color="robotsRankColor[record.rank]" bordered>
          {{ record.rank }}
        </a-tag>
      </template>
      <template #quality="{ record }">
        <a-tag :color="robotsQualityColor[record.quality]" bordered>
          {{ robotsQualityLabel[record.quality] }}
        </a-tag>
      </template>
      <template #repoUrl="{ record }">
        <a-link :href="record.repo_url" target="_blank">
          <template #icon>
            <icon-link />
          </template>
          visit
        </a-link>
      </template>
      <template #createdTime="{ record }">
        {{ dayjs(record.created_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #updatedTime="{ record }">
        {{ dayjs(record.updated_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #operations="{ record }">
        <icon-download
          class="custom-icon-button"
          @click="
            selectedRobotsMarketItem = record;
            installRobotsMarketModalVisible = true;
          "
        />
      </template>
    </a-table>
  </a-card>
  <a-modal
    v-model:visible="installRobotsMarketModalVisible"
    :mask-closable="false"
    :title="$t('common.install')"
    :ok-loading="robotsMarketTableLoading"
    @ok="installRobotsMarket(selectedRobotsMarketItem.repo_url)"
  >
    <a-space direction="vertical">
      <a-form-item required>
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
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import { robotsRankColor, robotsQualityColor } from '@/utils/func';
  import {
    apiGetRobotsMarketItems,
    apiInstallRobotsMarket,
  } from '@/api/robots/market';
  import { apiGetModelDetail } from '@/api/model';
  import ModelConfigSelect from '@/components/model/model-config-select/index.vue';
  import ModelConfigDetail from '@/components/model/model-config-detail/index.vue';
  import Empty from '@/components/empty/index.vue';

  const { t } = useI18n();

  const robotsMarketTableLoading = ref(false);

  const installRobotsMarketModalVisible = ref(false);

  const modelDetailLoading = ref(false);
  const modelDetail = ref<Record<string, any>>({});

  const selectedRobotsMarketItem = ref<Record<string, any>>({});
  const selectedModelConfig = ref('');
  const robotsMarketItems = ref<Record<string, any>[]>([]);
  const robotsMarketTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const robotsMarketTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const robotsRankOptions = ref(
    Array.from({ length: 9 }, (_, i) => ({
      label: `L${i + 1}`,
      value: `L${i + 1}`,
    }))
  );

  // 数字员工品质 label
  const robotsQualityLabel: Record<string, any> = {
    common: t('robots.quality.common'),
    uncommon: t('robots.quality.uncommon'),
    epic: t('robots.quality.epic'),
    rare: t('robots.quality.rare'),
    legendary: t('robots.quality.legendary'),
  };

  const robotsQualityOptions = computed<Record<string, any>[]>(() =>
    Object.keys(robotsQualityLabel).map((key) => ({
      value: key,
      label: robotsQualityLabel[key],
    }))
  );

  const robotsMarketSearchFormModel = ref<Record<string, any>>({
    name: '',
    description: '',
    author: '',
    department: '',
    ranks: [],
    qualities: [],
    createdTime: [],
    updatedTime: [],
  });

  const robotsMarketTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('robots.name'),
      dataIndex: 'name',
      ellipsis: true,
      tooltip: true,
      slotName: 'name',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      width: 300,
    },
    {
      title: t('robots.description'),
      dataIndex: 'description',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('robots.author'),
      dataIndex: 'author',
      ellipsis: true,
      tooltip: true,
      slotName: 'author',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('robots.department'),
      dataIndex: 'department',
      ellipsis: true,
      tooltip: true,
      slotName: 'department',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('robots.rank'),
      dataIndex: 'rank',
      slotName: 'rank',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('robots.quality'),
      dataIndex: 'quality',
      slotName: 'quality',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('robots.market.repoUrl'),
      dataIndex: 'repo_url',
      slotName: 'repoUrl',
      align: 'center',
    },
    {
      title: t('common.time.created'),
      dataIndex: 'created_time',
      slotName: 'createdTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('common.time.updated'),
      dataIndex: 'updated_time',
      slotName: 'updatedTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('common.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      align: 'center',
    },
  ]);

  // 获取数字员工列表查询参数
  const getRobotsMarketQueryParams = () => {
    const name = robotsMarketSearchFormModel.value.name.trim();
    const description = robotsMarketSearchFormModel.value.description.trim();
    const author = robotsMarketSearchFormModel.value.author.trim();
    const department = robotsMarketSearchFormModel.value.department.trim();
    const { ranks, qualities, createdTime, updatedTime } =
      robotsMarketSearchFormModel.value;
    const { orderBy, orderType } = robotsMarketTableOrder.value;

    const params: Record<string, any> = {
      page: robotsMarketTablePagination.value.current,
      size: robotsMarketTablePagination.value.pageSize,
    };

    if (name !== '') {
      params.name = name;
    }
    if (description !== '') {
      params.description = description;
    }
    if (author !== '') {
      params.author = author;
    }
    if (department !== '') {
      params.department = department;
    }
    if (ranks.length !== 0) {
      params.ranks = ranks;
    }
    if (qualities.length !== 0) {
      params.qualities = qualities;
    }
    if (createdTime.length !== 0) {
      [params.start_created_time, params.end_created_time] = createdTime;
    }
    if (updatedTime.length !== 0) {
      [params.start_updated_time, params.end_updated_time] = updatedTime;
    }

    if (orderBy !== '' && orderType !== '') {
      params.order_by = orderBy;
      params.order_type = orderType;
    }

    return params;
  };

  // 获取数字员工市场清单
  const getRobotsMarketItems = async () => {
    robotsMarketTableLoading.value = true;
    try {
      const params = getRobotsMarketQueryParams();
      const { data } = await apiGetRobotsMarketItems(params);

      robotsMarketItems.value = data.items;
      robotsMarketTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsMarketTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeRobotsMarketTablePage = async (page: number) => {
    robotsMarketTableLoading.value = true;
    robotsMarketTablePagination.value.current = page;
    await getRobotsMarketItems();
    robotsMarketTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeRobotsMarketTablePageSize = async (pageSize: number) => {
    robotsMarketTableLoading.value = true;
    robotsMarketTablePagination.value.pageSize = pageSize;
    await getRobotsMarketItems();
    robotsMarketTableLoading.value = false;
  };

  // 切换表格排序
  const changeRobotsMarketTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    robotsMarketTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      robotsMarketTableOrder.value.orderBy = dataIndex;
      robotsMarketTableOrder.value.orderType =
        direction === 'ascend' ? 'asc' : 'desc';
    } else {
      robotsMarketTableOrder.value.orderBy = '';
      robotsMarketTableOrder.value.orderType = '';
    }
    await getRobotsMarketItems();
    robotsMarketTableLoading.value = false;
  };

  // 重置搜索表单
  const resetRobotsMarketSearchFormModel = async () => {
    robotsMarketTableLoading.value = true;
    robotsMarketSearchFormModel.value.name = '';
    robotsMarketSearchFormModel.value.description = '';
    robotsMarketSearchFormModel.value.author = '';
    robotsMarketSearchFormModel.value.department = '';
    robotsMarketSearchFormModel.value.ranks = [];
    robotsMarketSearchFormModel.value.qualities = [];
    robotsMarketSearchFormModel.value.createdTime = [];
    robotsMarketSearchFormModel.value.updatedTime = [];
    await getRobotsMarketItems();
    robotsMarketTableLoading.value = false;
  };

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

  // 安装数字员工
  const installRobotsMarket = async (url: string) => {
    robotsMarketTableLoading.value = true;
    try {
      const params = {
        url,
        model_config_id: selectedModelConfig.value,
      };
      await apiInstallRobotsMarket(params);
      await getRobotsMarketItems();
      installRobotsMarketModalVisible.value = false;
      Message.success(t('common.install.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsMarketTableLoading.value = false;
    }
  };

  onMounted(() => {
    getRobotsMarketItems();
  });

  watch(
    () => selectedModelConfig.value,
    () => {
      getModelDetail();
    }
  );
</script>

<style scoped lang="less">
  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
</style>
