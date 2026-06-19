<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    :footer="false"
    width="90%"
    :title="$t('skills.market')"
    title-align="start"
    @cancel="emit('close')"
  >
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="skillsMarketSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="16">
            <a-col :span="24">
              <a-form-item field="q" :label="$t('common.keyword')" required>
                <a-input
                  v-model="skillsMarketSearchFormModel.q"
                  :placeholder="$t('common.keyword.placeholder')"
                  allow-clear
                  @keyup.enter="getSkillsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="16">
              <a-form-item field="category" :label="$t('skills.category')">
                <a-input
                  v-model="skillsMarketSearchFormModel.category"
                  :placeholder="$t('skills.category.placeholder')"
                  allow-clear
                  @keyup.enter="getSkillsMarketItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item field="occupation" :label="$t('skills.occupation')">
                <a-input
                  v-model="skillsMarketSearchFormModel.occupation"
                  :placeholder="$t('skills.occupation.placeholder')"
                  allow-clear
                  @keyup.enter="getSkillsMarketItems"
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
            :loading="skillsMarketTableLoading"
            type="primary"
            @click="getSkillsMarketItems"
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            :loading="skillsMarketTableLoading"
            @click="resetSkillsMarketSearchFormModel"
          >
            <template #icon>
              <icon-refresh />
            </template>
            {{ $t('common.reset') }}
          </a-button>
        </a-space>
      </a-col>
    </a-row>
    <a-table
      v-model:selected-keys="skillsMarketTableSelectedKeys"
      style="height: 70vh"
      row-key="name"
      :scroll="{ y: 'calc(88vh - 300px)' }"
      :loading="skillsMarketTableLoading"
      :pagination="skillsMarketTablePagination"
      :columns="skillsMarketTableColumns"
      :data="skillsMarketItems"
      :bordered="false"
      @page-change="changeSkillsMarketTablePage"
      @page-size-change="changeSkillsMarketTablePageSize"
      @sorter-change="changeSkillsMarketTableOrder"
    >
      <template #index="{ rowIndex }">
        {{
          rowIndex +
          1 +
          (skillsMarketTablePagination.current - 1) *
            skillsMarketTablePagination.pageSize
        }}
      </template>
      <template #name="{ record }">
        <a-tag color="orangered" bordered>
          <template #icon> <icon-tool /> </template>
          {{ record.name }}
        </a-tag>
      </template>
      <template #author="{ record }">
        <span :style="{ display: 'flex', alignItems: 'center' }">
          <a-avatar
            :style="{
              marginRight: '8px',
              backgroundColor: generateColor(record.author),
            }"
            :size="25"
          >
            {{
              record.author.charAt(0).toUpperCase() + record.author.charAt(1)
            }}
          </a-avatar>
          {{ record.author }}
        </span>
      </template>
      <template #githubUrl="{ record }">
        <a-link :href="record.githubUrl" target="_blank">
          <template #icon>
            <icon-github />
          </template>
          Github
        </a-link>
      </template>
      <template #skillUrl="{ record }">
        <a-link :href="record.skillUrl" target="_blank" icon> visit </a-link>
      </template>
      <template #stars="{ record }">
        <a-tag color="red" bordered>
          <template #icon> <icon-heart /> </template>{{ record.stars }}
        </a-tag>
      </template>
      <template #updatedAt="{ record }">
        {{ dayjs(record.updatedAt).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #operations="{ record }">
        <a-popconfirm
          type="warning"
          :content="$t('common.confirm.install')"
          @ok="installFromSkillsMarket(record.githubUrl)"
          @ok-loading="skillsMarketTableLoading"
        >
          <a-tooltip :content="$t('common.install')">
            <icon-download class="custom-icon-button" />
          </a-tooltip>
        </a-popconfirm>
      </template>
    </a-table>
  </a-modal>
</template>

<script setup lang="ts">
  import { computed, ref, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import { apiGetSkillsmpItems, apiInstallSkillsmp } from '@/api/skills';
  import { generateColor } from '@marko19907/string-to-color';
  import dayjs from 'dayjs';

  const { t } = useI18n();

  const props = defineProps<{ category: string }>();
  const emit = defineEmits<{ close: []; refresh: [] }>();

  const skillsMarketTableLoading = ref(false);

  const skillsMarketItems = ref<Record<string, any>[]>([]);
  const skillsMarketTableSelectedKeys = ref<string[]>([]);
  const skillsMarketTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 20,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const skillsMarketTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const skillsMarketSearchFormModel = ref<Record<string, any>>({
    q: 'default',
    category: '',
    occupation: '',
  });

  const skillsMarketTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('skills.name'),
      dataIndex: 'name',
      ellipsis: true,
      tooltip: true,
      slotName: 'name',
      align: 'center',
    },
    {
      title: t('skills.market.table.author'),
      dataIndex: 'author',
      slotName: 'author',
    },
    {
      title: t('skills.description'),
      dataIndex: 'description',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('skills.market.table.githubUrl'),
      dataIndex: 'githubUrl',
      slotName: 'githubUrl',
      align: 'center',
      width: 120,
    },
    {
      title: t('skills.market.table.skillUrl'),
      dataIndex: 'skillUrl',
      slotName: 'skillUrl',
      align: 'center',
      width: 120,
    },
    {
      title: t('skills.market.table.stars'),
      dataIndex: 'stars',
      slotName: 'stars',
      sortable: {
        sortDirections: ['descend'],
        sorter: true,
      },
      align: 'center',
      width: 120,
    },
    {
      title: t('common.time.updated'),
      dataIndex: 'updatedAt',
      slotName: 'updatedAt',
      sortable: {
        sortDirections: ['descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('common.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      align: 'center',
      width: 100,
    },
  ]);

  // 获取技能市场列表查询参数
  const getSkillsMarketQueryParams = () => {
    const q = skillsMarketSearchFormModel.value.q.trim();
    const category = skillsMarketSearchFormModel.value.category.trim();
    const occupation = skillsMarketSearchFormModel.value.occupation.trim();
    const { orderBy } = skillsMarketTableOrder.value;

    const params: Record<string, any> = {
      page: skillsMarketTablePagination.value.current,
      limit: skillsMarketTablePagination.value.pageSize,
      q,
    };

    if (category !== '') {
      params.category = category;
    }
    if (occupation !== '') {
      params.occupation = occupation;
    }

    if (orderBy !== '') {
      params.sortBy = orderBy;
    }

    return params;
  };

  // 获取技能市场列表
  const getSkillsMarketItems = async () => {
    skillsMarketTableLoading.value = true;
    try {
      const params = getSkillsMarketQueryParams();
      const { data } = await apiGetSkillsmpItems(params);

      skillsMarketItems.value = data.items;
      skillsMarketTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsMarketTableLoading.value = false;
    }
  };

  // 切换技能市场表格分页
  const changeSkillsMarketTablePage = async (page: number) => {
    skillsMarketTableLoading.value = true;
    skillsMarketTablePagination.value.current = page;
    await getSkillsMarketItems();
    skillsMarketTableLoading.value = false;
  };

  // 切换技能市场表格每页条数
  const changeSkillsMarketTablePageSize = async (pageSize: number) => {
    skillsMarketTableLoading.value = true;
    skillsMarketTablePagination.value.pageSize = pageSize;
    await getSkillsMarketItems();
    skillsMarketTableLoading.value = false;
  };

  // 切换技能市场表格排序
  const changeSkillsMarketTableOrder = async (dataIndex: string) => {
    skillsMarketTableLoading.value = true;
    if (dataIndex === 'updateAt') {
      skillsMarketTableOrder.value.orderBy = 'recent';
    } else {
      skillsMarketTableOrder.value.orderBy = dataIndex;
    }
    await getSkillsMarketItems();
    skillsMarketTableLoading.value = false;
  };

  // 重置技能市场搜索表单
  const resetSkillsMarketSearchFormModel = async () => {
    skillsMarketTableLoading.value = true;
    skillsMarketSearchFormModel.value.q = 'default';
    skillsMarketSearchFormModel.value.category = '';
    skillsMarketSearchFormModel.value.occupation = '';
    await getSkillsMarketItems();
    skillsMarketTableLoading.value = false;
  };

  // 从技能市场安装技能
  const installFromSkillsMarket = async (githubUrl: string) => {
    skillsMarketTableLoading.value = true;
    try {
      const params: Record<string, any> = {
        url: githubUrl,
      };
      if (props.category !== '#default') {
        params.category = props.category;
      }
      await apiInstallSkillsmp(params);
      Message.success(t('common.install.success'));
      emit('refresh');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsMarketTableLoading.value = false;
    }
  };

  onMounted(() => {
    getSkillsMarketItems();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }

  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
</style>
