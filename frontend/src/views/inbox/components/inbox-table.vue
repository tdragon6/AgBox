<template>
  <div class="container">
    <a-card :style="{ height: '88vh' }" :title="$t('inbox.items')">
      <div v-if="props.selectedRobot !== ''">
        <a-row>
          <a-col :flex="1">
            <a-form
              :model="inboxSearchFormModel"
              auto-label-width
              label-align="left"
            >
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-form-item field="types" :label="$t('inbox.type')">
                    <a-select
                      v-model="inboxSearchFormModel.types"
                      :placeholder="$t('inbox.type.select.placeholder')"
                      multiple
                      allow-clear
                    >
                      <a-option
                        v-for="item in inboxTypeOptions"
                        :key="item.value"
                        :value="item.value"
                        :tag-props="{ color: inboxTypeColor[item.value] }"
                      >
                        <a-tag :color="inboxTypeColor[item.value]">
                          {{ item.label }}
                        </a-tag>
                      </a-option>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item field="statuses" :label="$t('inbox.status')">
                    <a-select
                      v-model="inboxSearchFormModel.statuses"
                      :placeholder="$t('inbox.status.select.placeholder')"
                      multiple
                      allow-clear
                    >
                      <a-option
                        v-for="item in inboxStatusOptions"
                        :key="item.value"
                        :value="item.value"
                        :tag-props="{ color: inboxStatusColor[item.value] }"
                      >
                        <a-tag :color="inboxStatusColor[item.value]">
                          {{ item.label }}
                        </a-tag>
                      </a-option>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item
                    field="createdTime"
                    :label="$t('common.time.created')"
                  >
                    <a-range-picker
                      v-model="inboxSearchFormModel.createdTime"
                      show-time
                      :time-picker-props="{
                        defaultValue: ['00:00:00', '00:00:00'],
                      }"
                      style="width: 100%"
                    />
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item field="message" :label="$t('tasks.message')">
                    <a-input
                      v-model="inboxSearchFormModel.message"
                      :placeholder="$t('tasks.message.placeholder')"
                      allow-clear
                      @keyup.enter="getInboxItems"
                    />
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item field="isRead" :label="$t('inbox.isRead')">
                    <a-select
                      v-model="inboxSearchFormModel.isRead"
                      :options="isReadOptions"
                      :placeholder="$t('inbox.isRead.select.placeholder')"
                      allow-clear
                    >
                      <template #label="{ data }">
                        <a-badge
                          :text="$t(data.label)"
                          :status="data.value === true ? 'success' : 'normal'"
                        />
                      </template>
                      <template #option="{ data }">
                        <a-badge
                          :text="$t(data.label)"
                          :status="data.value === true ? 'success' : 'normal'"
                        />
                      </template>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item
                    field="updatedTime"
                    :label="$t('common.time.updated')"
                  >
                    <a-range-picker
                      v-model="inboxSearchFormModel.updatedTime"
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
                :loading="inboxTableLoading"
                type="primary"
                @click="getInboxItems"
              >
                <template #icon>
                  <icon-search />
                </template>
                {{ $t('common.search') }}
              </a-button>
              <a-button
                v-debounce
                :loading="inboxTableLoading"
                @click="resetInboxSearchFormModel"
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
        <a-row style="margin-bottom: 16px">
          <a-col :span="12">
            <a-space>
              <a-button
                v-debounce
                size="small"
                type="outline"
                @click="updateInboxReadStatus(inboxItems)"
              >
                <template #icon>
                  <icon-check />
                </template>
                {{ $t('inbox.read.all') }}
              </a-button>
            </a-space>
          </a-col>
          <a-col
            :span="12"
            style="display: flex; align-items: center; justify-content: end"
          >
            <a-popconfirm
              type="warning"
              :content="$t('common.confirm.delete')"
              @ok="deleteInbox(inboxTableSelectedKeys)"
              @ok-loading="inboxTableLoading"
            >
              <a-button
                :disabled="inboxTableSelectedKeys.length === 0"
                :loading="inboxTableLoading"
                size="small"
                type="outline"
                status="danger"
              >
                <template #icon>
                  <icon-delete />
                </template>
                {{ $t('common.delete.batch') }}
              </a-button>
            </a-popconfirm>
          </a-col>
        </a-row>
        <a-table
          v-model:selected-keys="inboxTableSelectedKeys"
          :row-class="rowClass"
          row-key="id"
          :row-selection="{
            type: 'checkbox',
            showCheckedAll: true,
          }"
          :scroll="{ y: 'calc(75vh - 300px)' }"
          :loading="inboxTableLoading"
          :pagination="inboxTablePagination"
          :columns="inboxTableColumns"
          :data="inboxItems"
          :bordered="false"
          @page-change="changeInboxTablePage"
          @page-size-change="changeInboxTablePageSize"
          @sorter-change="changeInboxTableOrder"
        >
          <template #index="{ rowIndex }">
            {{
              rowIndex +
              1 +
              (inboxTablePagination.current - 1) * inboxTablePagination.pageSize
            }}
          </template>
          <template #robot="{ record }">
            <a-tag
              v-if="record.coordinator === true"
              :color="tasksTypeColor[record.robot]"
            >
              {{ $t(coordinatorName[record.robot]) }}
            </a-tag>
            <span v-else>
              <Media
                :style="{
                  backgroundColor: 'var(--color-bg-2)',
                }"
                :size="25"
                :url="apiGetRobotsManageAvatarUrl({ name: record.robot })"
                scope="avatar"
              />
              {{ record.robot }}
            </span>
          </template>
          <template #type="{ record }">
            <a-tag :color="inboxTypeColor[record.type]" bordered>
              {{
                $t(
                  inboxTypeOptions.find((item) => item.value === record.type)
                    ?.label ?? ''
                )
              }}
            </a-tag>
          </template>
          <template #status="{ record }">
            <a-tag :color="inboxStatusColor[record.status]" bordered>
              {{
                record.type === 'tasks'
                  ? record.status
                  : $t(`robots.${record.status}`)
              }}
            </a-tag>
          </template>
          <template #isRead="{ record }">
            <a-badge
              :text="$t(`common.${record.is_read}`)"
              :status="record.is_read === true ? 'normal' : 'warning'"
            />
          </template>
          <template #createdTime="{ record }">
            {{ dayjs(record.created_time).format('YYYY-MM-DD HH:mm:ss') }}
          </template>
          <template #updatedTime="{ record }">
            {{ dayjs(record.updated_time).format('YYYY-MM-DD HH:mm:ss') }}
          </template>
          <template #operations="{ record }">
            <a-button
              v-debounce
              type="text"
              size="small"
              @click="
                updateInboxReadStatus([record]);
                selectedInboxItem = record;
                inboxResultModalVisible = true;
              "
            >
              {{ $t('common.view') }}
            </a-button>
            <a-popconfirm
              type="warning"
              :content="$t('common.confirm.delete')"
              @ok="deleteInbox([record.id])"
              @ok-loading="inboxTableLoading"
            >
              <a-button
                :loading="inboxTableLoading"
                type="text"
                status="danger"
                size="small"
              >
                {{ $t('common.delete') }}
              </a-button>
            </a-popconfirm>
          </template>
        </a-table>
      </div>
      <Empty v-else />
    </a-card>
  </div>
  <a-modal
    v-model:visible="inboxResultModalVisible"
    :title="$t('inbox.detail.result')"
    :mask-closable="false"
    :footer="false"
    width="60%"
  >
    <div v-if="inboxResultModalVisible === true">
      <MdPreview
        v-if="selectedInboxItem.type === 'tasks'"
        :model-value="selectedInboxItem.result"
        show-code-row-number
        :sanitizer="(html: string) => DOMPurify.sanitize(html)"
        style="max-height: 80vh"
      />
      <InboxDetailUpgrade v-else :selected-inbox-item="selectedInboxItem" />
    </div>
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    tasksTypeColor,
    coordinatorName,
    inboxTypeColor,
    inboxStatusColor,
  } from '@/utils/func';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import {
    apiGetInboxItems,
    apiDeleteInbox,
    apiUpdateInboxReadStatus,
  } from '@/api/inbox';
  import Media from '@/components/media/index.vue';
  import { MdPreview } from 'md-editor-v3';
  import 'md-editor-v3/lib/style.css';
  import DOMPurify from 'dompurify';
  import Empty from '@/components/empty/index.vue';
  import InboxDetailUpgrade from '@/views/inbox/components/inbox-detail-upgrade.vue';
  import useUnreadRobotsInboxCountStore from '@/store/modules/inbox';

  const { t } = useI18n();

  const unreadRobotsInboxCount = useUnreadRobotsInboxCountStore();

  const props = defineProps<{
    selectedRobot: string;
  }>();

  const inboxTableLoading = ref(false);

  const inboxResultModalVisible = ref(false);

  const rowClass = (record: Record<string, any>) => {
    return record.is_read === true ? 'inbox-row-read' : '';
  };

  const selectedInboxItem = ref<Record<string, any>>({});

  const inboxTableSelectedKeys = ref<string[]>([]);
  const inboxItems = ref<Record<string, any>[]>([]);
  const inboxTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });

  const inboxTypeOptions = computed(() => [
    {
      value: 'tasks',
      label: t('inbox.type.tasks'),
    },
    {
      value: 'upgrade',
      label: t('inbox.type.upgrade'),
    },
  ]);

  const isReadOptions = computed<Record<string, any>[]>(() => [
    {
      label: t('common.true'),
      value: true,
    },
    {
      label: t('common.false'),
      value: false,
    },
  ]);

  const inboxStatusOptions = computed(() => {
    const options: Record<string, any>[] = [
      {
        value: 'finished',
        label: 'finished',
      },
      {
        value: 'interrupted',
        label: 'interrupted',
      },
      {
        value: 'failed',
        label: 'failed',
      },
    ];

    if (props.selectedRobot.startsWith('#')) {
      options.push(
        {
          value: 'rank',
          label: t('robots.rank'),
        },
        {
          value: 'quality',
          label: t('robots.quality'),
        }
      );
    }
    return options;
  });

  const inboxSearchFormModel = ref<Record<string, any>>({
    types: [],
    message: '',
    statuses: [],
    isRead: '',
    createdTime: [],
    updatedTime: [],
  });
  const inboxTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const inboxTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('robots.name'),
      dataIndex: 'robot',
      slotName: 'robot',
      ellipsis: true,
      tooltip: true,
      align: 'center',
    },
    {
      title: t('inbox.type'),
      dataIndex: 'type',
      slotName: 'type',
      align: 'center',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('tasks.message'),
      dataIndex: 'message',
      ellipsis: true,
      tooltip: true,
      align: 'center',
    },
    {
      title: t('inbox.status'),
      dataIndex: 'status',
      slotName: 'status',
      align: 'center',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('inbox.isRead'),
      dataIndex: 'is_read',
      slotName: 'isRead',
      align: 'center',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('common.time.created'),
      dataIndex: 'created_time',
      slotName: 'createdTime',
      align: 'center',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('common.time.updated'),
      dataIndex: 'updated_time',
      slotName: 'updatedTime',
      align: 'center',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('common.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      align: 'center',
    },
  ]);

  // 获取收件箱列表查询参数
  const getInboxItemsQueryParams = () => {
    const message = inboxSearchFormModel.value.message.trim();
    const { types, statuses, isRead, createdTime, updatedTime } =
      inboxSearchFormModel.value;
    const { orderBy, orderType } = inboxTableOrder.value;

    const params: Record<string, any> = {
      page: inboxTablePagination.value.current,
      size: inboxTablePagination.value.pageSize,
      robot: props.selectedRobot.startsWith('#')
        ? props.selectedRobot.slice(1)
        : props.selectedRobot,
      coordinator: props.selectedRobot.startsWith('#'),
    };

    if (types.length !== 0) {
      params.types = types;
    }
    if (statuses.length !== 0) {
      params.statuses = statuses;
    }
    if (message !== '') {
      params.message = message;
    }
    if (isRead !== '') {
      params.is_read = isRead;
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

  // 获取收件箱列表
  const getInboxItems = async () => {
    inboxTableLoading.value = true;
    try {
      const params = getInboxItemsQueryParams();
      const { data } = await apiGetInboxItems(params);

      inboxItems.value = data.items;
      inboxTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      inboxTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeInboxTablePage = async (page: number) => {
    inboxTableLoading.value = true;
    inboxTablePagination.value.current = page;
    await getInboxItems();
    inboxTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeInboxTablePageSize = async (pageSize: number) => {
    inboxTableLoading.value = true;
    inboxTablePagination.value.pageSize = pageSize;
    await getInboxItems();
    inboxTableLoading.value = false;
  };

  // 切换表格排序
  const changeInboxTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    inboxTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      inboxTableOrder.value.orderBy = dataIndex;
      inboxTableOrder.value.orderType = direction === 'ascend' ? 'asc' : 'desc';
    } else {
      inboxTableOrder.value.orderBy = '';
      inboxTableOrder.value.orderType = '';
    }
    await getInboxItems();
    inboxTableLoading.value = false;
  };

  // 重置搜索表单
  const resetInboxSearchFormModel = async () => {
    inboxTableLoading.value = true;
    inboxSearchFormModel.value.types = [];
    inboxSearchFormModel.value.message = '';
    inboxSearchFormModel.value.statuses = [];
    inboxSearchFormModel.value.isRead = '';
    inboxSearchFormModel.value.createdTime = [];
    inboxSearchFormModel.value.updatedTime = [];
    await getInboxItems();
    inboxTableLoading.value = false;
  };

  // 删除收件箱通知
  const deleteInbox = async (ids: string[]) => {
    inboxTableLoading.value = true;
    try {
      const params = {
        ids,
      };
      await apiDeleteInbox(params);
      await getInboxItems();
      await unreadRobotsInboxCount.getUnreadRobotsInboxCount();
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      inboxTableSelectedKeys.value = [];
      inboxTableLoading.value = false;
    }
  };

  // 更新收件箱通知已读状态
  const updateInboxReadStatus = async (items: Record<string, any>[]) => {
    try {
      const ids: string[] = [];
      items.forEach((item) => ids.push(item.id));

      const params = {
        ids,
      };
      await apiUpdateInboxReadStatus(params);
      unreadRobotsInboxCount.getUnreadRobotsInboxCount();
      items.forEach((item) => {
        item.is_read = true;
      });

      getInboxItems();
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      inboxTableSelectedKeys.value = [];
      inboxTableLoading.value = false;
    }
  };

  onMounted(() => {
    getInboxItems();
  });

  watch(
    () => props.selectedRobot,
    () => {
      getInboxItems();
    }
  );
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

  :deep(.arco-table-tr.inbox-row-read) {
    .arco-table-td {
      background-color: var(--color-fill-1);
      color: var(--color-text-3);
    }
  }
</style>
