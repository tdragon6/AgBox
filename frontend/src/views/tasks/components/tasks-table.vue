<template>
  <a-row>
    <a-col :flex="1">
      <a-form :model="tasksSearchFormModel" auto-label-width label-align="left">
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item field="priorities" :label="$t('tasks.priority')">
              <PrioritySelect
                v-model="tasksSearchFormModel.priorities"
                :multiple="true"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="statuses" :label="$t('tasks.status')">
              <a-select
                v-model="tasksSearchFormModel.statuses"
                :placeholder="$t('tasks.status.placeholder')"
                multiple
                allow-clear
              >
                <a-option
                  v-for="item in tasksStatusOptions"
                  :key="item.value"
                  :value="item.value"
                >
                  <a-tag :color="tasksStatusColor[item.value]">
                    {{ item.label }}
                  </a-tag>
                </a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="createdTime" :label="$t('common.time.created')">
              <a-range-picker
                v-model="tasksSearchFormModel.createdTime"
                show-time
                :time-picker-props="{
                  defaultValue: ['00:00:00', '00:00:00'],
                }"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="triggers" :label="$t('tasks.trigger')">
              <a-select
                v-model="tasksSearchFormModel.triggers"
                :placeholder="$t('tasks.trigger.placeholder')"
                multiple
                allow-clear
              >
                <a-option
                  v-for="item in tasksTriggerOptions"
                  :key="item.value"
                  :value="item.value"
                  :tag-props="{ color: tasksTriggerColor[item.value] }"
                >
                  <a-tag :color="tasksTriggerColor[item.value]">
                    {{ item.label }}
                  </a-tag>
                </a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="message" :label="$t('tasks.message')">
              <a-input
                v-model="tasksSearchFormModel.message"
                :placeholder="$t('tasks.message.placeholder')"
                allow-clear
                @keyup.enter="getTasksItems"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item field="updatedTime" :label="$t('common.time.updated')">
              <a-range-picker
                v-model="tasksSearchFormModel.updatedTime"
                show-time
                :time-picker-props="{
                  defaultValue: ['00:00:00', '00:00:00'],
                }"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item
              v-if="props.scope !== 'session'"
              field="types"
              :label="$t('tasks.type')"
            >
              <a-select
                v-model="tasksSearchFormModel.types"
                :placeholder="$t('tasks.type.placeholder')"
                multiple
                allow-clear
              >
                <a-option
                  v-for="item in tasksTypeOptions"
                  :key="item.value"
                  :value="item.value"
                  :tag-props="{ color: tasksTypeColor[item.value] }"
                >
                  <a-tag :color="tasksTypeColor[item.value]">
                    {{ item.label }}
                  </a-tag>
                </a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col v-if="props.scope !== 'session'" :span="8">
            <a-form-item field="robots" :label="$t('robots.name')">
              <RobotsSelect
                v-model:selected-robots="tasksSearchFormModel.robots"
                :multiple="true"
                :selected-project-item="selectedSessionItem"
                :scope="props.scope === 'dashboard' ? 'robot' : 'project'"
              />
            </a-form-item>
          </a-col>
          <a-col v-else :span="6"></a-col>
        </a-row>
      </a-form>
    </a-col>
    <a-divider
      :style="{ height: props.scope !== 'session' ? '135px' : '85px' }"
      direction="vertical"
    />
    <a-col :flex="'86px'" style="text-align: right">
      <a-space direction="vertical" :size="18">
        <a-button
          v-debounce
          :loading="tasksTableLoading"
          type="primary"
          @click="getTasksItems"
        >
          <template #icon>
            <icon-search />
          </template>
          {{ $t('common.search') }}
        </a-button>
        <a-button
          v-debounce
          :loading="tasksTableLoading"
          @click="resetTasksSearchFormModel"
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
      <a-button
        v-debounce
        size="small"
        type="primary"
        @click="createTasksModalVisible = true"
      >
        <template #icon>
          <icon-plus />
        </template>
        {{ $t('common.create') }}
      </a-button>
    </a-col>
    <a-col
      :span="12"
      style="display: flex; align-items: center; justify-content: end"
    >
      <a-popconfirm
        type="warning"
        :content="$t('tasks.confirm.cancel')"
        @ok="cancelTasks(tasksTableSelectedKeys)"
        @ok-loading="tasksTableLoading"
      >
        <a-button
          :disabled="
            tasksTableSelectedKeys.length === 0 ||
            tasksTableSelectedKeys.some(
              (key) =>
                ['running', 'pending'].includes(
                  tasksItems.find((item) => item.id === key)?.status
                ) === false
            )
          "
          :loading="tasksTableLoading"
          size="small"
          type="outline"
          status="danger"
        >
          <template #icon>
            <icon-close-circle />
          </template>
          {{ $t('tasks.cancel.batch') }}
        </a-button>
      </a-popconfirm>
    </a-col>
  </a-row>
  <a-table
    v-model:selected-keys="tasksTableSelectedKeys"
    row-key="id"
    :row-selection="{
      type: 'checkbox',
      showCheckedAll: true,
    }"
    :scroll="{ y: 'calc(88vh - 300px)' }"
    :loading="tasksTableLoading"
    :pagination="tasksTablePagination"
    :columns="tasksTableColumns"
    :data="tasksItems"
    :bordered="false"
    @page-change="changeTasksTablePage"
    @page-size-change="changeTasksTablePageSize"
    @sorter-change="changeTasksTableOrder"
  >
    <template #index="{ rowIndex }">
      {{
        rowIndex +
        1 +
        (tasksTablePagination.current - 1) * tasksTablePagination.pageSize
      }}
    </template>
    <template v-if="props.scope !== 'session'" #robots="{ record }">
      <a-avatar-group
        :size="30"
        :max-count="2"
        :style="{ display: 'flex', alignItems: 'center' }"
      >
        <a-tooltip
          v-for="robotItem in record.robots"
          :key="robotItem"
          :content="robotItem"
        >
          <Media
            :style="{
              backgroundColor: 'var(--color-bg-2)',
            }"
            :size="35"
            :url="apiGetRobotsManageAvatarUrl({ name: robotItem })"
            scope="avatar"
          />
        </a-tooltip>
      </a-avatar-group>
    </template>
    <template v-if="props.scope !== 'session'" #type="{ record }">
      <a-tag :color="tasksTypeColor[record.type]" bordered>
        {{ tasksTypeOptions.find((item) => item.value === record.type)?.label }}
      </a-tag>
    </template>
    <template #priority="{ record }">
      <a-space>
        <a-tag :color="tasksPriorityColor[record.priority]" bordered>
          {{ record.priority }}
        </a-tag>
        <a-tooltip
          v-if="record.status === 'pending'"
          :content="$t('tasks.priority.update')"
        >
          <icon-edit
            v-debounce
            class="custom-icon-button"
            @click="
              selectedTasksItem = record;
              updateTasksPriorityModalVisible = true;
            "
          />
        </a-tooltip>
      </a-space>
    </template>
    <template #status="{ record }">
      <a-tag :color="tasksStatusColor[record.status]" bordered>
        {{ record.status }}
      </a-tag>
    </template>
    <template #trigger="{ record }">
      <a-tag :color="tasksTriggerColor[record.trigger]" bordered>
        {{ record.trigger }}
      </a-tag>
    </template>
    <template #createdTime="{ record }">
      {{
        dayjs(record.created_time).isValid()
          ? dayjs(record.created_time).format('YYYY-MM-DD HH:mm:ss')
          : '-'
      }}
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
          async () => {
            selectedTasksItem = record;
            tasksViewModalVisible = true;
            tasksResult = (await apiGetTasksResult({ id: record.id })).data;
          }
        "
      >
        {{ $t('common.view') }}
      </a-button>
      <a-popconfirm
        v-if="record.status === 'running' || record.status === 'pending'"
        type="warning"
        :content="$t('tasks.confirm.cancel')"
        @ok="cancelTasks([record.id])"
        @ok-loading="tasksTableLoading"
      >
        <a-button
          :loading="tasksTableLoading"
          type="text"
          status="danger"
          size="small"
        >
          {{ $t('tasks.cancel') }}
        </a-button>
      </a-popconfirm>
    </template>
  </a-table>
  <a-modal
    v-model:visible="updateTasksPriorityModalVisible"
    :mask-closable="false"
    :title="$t('tasks.priority.update')"
    :ok-loading="tasksTableLoading"
    @ok="updateTasksPriority(selectedTasksItem.id)"
  >
    <a-form-item :label="$t('tasks.priority')" required>
      <PrioritySelect v-model="selectedUpdateTasksPriority" :multiple="false" />
    </a-form-item>
  </a-modal>
  <TasksInput
    v-if="createTasksModalVisible === true"
    :session-item="props.selectedSessionItem"
    :robot="props.scope === 'project' ? '#agbox-coordinator-sync' : props.robot"
    @close="createTasksModalVisible = false"
    @refresh="getTasksItems"
  />
  <a-modal
    v-model:visible="tasksViewModalVisible"
    :title="$t('tasks.detail')"
    :mask-closable="false"
    :footer="false"
    width="60%"
  >
    <a-tabs v-model:active-key="tasksViewTabKey" style="height: 85vh">
      <a-tab-pane key="result" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-info-circle /> {{ $t('tasks.result') }} </a-space>
        </template>
        <MdPreview
          v-if="tasksViewModalVisible === true && tasksViewTabKey === 'result'"
          :model-value="tasksResult"
          show-code-row-number
          :sanitizer="(html: string) => DOMPurify.sanitize(html)"
          style="max-height: 75vh; overflow: auto"
        />
      </a-tab-pane>
      <a-tab-pane key="message" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-message /> {{ $t('tasks.message') }} </a-space>
        </template>
        <TasksMessages
          v-if="tasksViewModalVisible === true && tasksViewTabKey === 'message'"
          :selected-tasks-or-session-item="selectedTasksItem"
          :robot="props.robot"
        />
      </a-tab-pane>
    </a-tabs>
  </a-modal>
</template>

<script setup lang="ts">
  import { computed, ref, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    tasksTypeColor,
    coordinatorName,
    tasksPriorityColor,
    tasksStatusColor,
    tasksTriggerColor,
  } from '@/utils/func';
  import {
    apiGetTasksItems,
    apiCancelTasks,
    apiUpdateTasksPriority,
    apiGetTasksResult,
  } from '@/api/tasks/task';
  import { MdPreview } from 'md-editor-v3';
  import 'md-editor-v3/lib/style.css';
  import DOMPurify from 'dompurify';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';
  import TasksInput from '@/components/tasks/tasks-input/index.vue';
  import Media from '@/components/media/index.vue';
  import PrioritySelect from '@/components/tasks/tasks-priority-select/index.vue';
  import TasksMessages from './tasks-messages.vue';

  const { t } = useI18n();

  const props = defineProps<{
    robot: string;
    selectedSessionItem: Record<string, any>;
    scope: 'session' | 'project' | 'dashboard';
  }>();

  const tasksResult = ref('');

  const tasksTableLoading = ref(false);

  const createTasksModalVisible = ref(false);
  const tasksViewModalVisible = ref(false);
  const updateTasksPriorityModalVisible = ref(false);

  const tasksViewTabKey = ref('result');
  const tasksTableSelectedKeys = ref<string[]>([]);
  const selectedTasksItem = ref<Record<string, any>>({});
  const tasksItems = ref<Record<string, any>[]>([]);
  const selectedUpdateTasksPriority = ref('P3');

  const tasksTypeOptions = computed<Record<string, any>[]>(() => {
    const options: Record<string, any>[] = [];
    Object.keys(coordinatorName).forEach((key) =>
      options.push({
        label: t(coordinatorName[key]),
        value: key,
      })
    );

    if (props.scope === 'dashboard') {
      options.push({
        label: t('tasks.session'),
        value: 'session',
      });
    }
    return options;
  });

  const tasksStatusOptions = ref<Record<string, any>[]>([
    {
      label: 'pending',
      value: 'pending',
    },
    {
      label: 'running',
      value: 'running',
    },
    {
      label: 'finished',
      value: 'finished',
    },
    {
      label: 'interrupted',
      value: 'interrupted',
    },
    {
      label: 'failed',
      value: 'failed',
    },
  ]);

  const tasksTriggerOptions = ref<Record<string, any>[]>([
    {
      label: 'user',
      value: 'user',
    },
    {
      label: 'scheduler',
      value: 'scheduler',
    },
  ]);

  const tasksSearchFormModel = ref<Record<string, any>>({
    message: '',
    types: [],
    priorities: [],
    statuses: [],
    triggers: [],
    robots: [],
    createdTime: [],
    updatedTime: [],
  });

  const tasksTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const tasksTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const tasksTableColumns = computed<TableColumnData[]>(() => {
    const baseColumns: TableColumnData[] = [
      {
        title: t('common.index'),
        dataIndex: 'index',
        slotName: 'index',
        width: 50,
        align: 'center',
      },
      {
        title: t('tasks.message'),
        dataIndex: 'message',
        ellipsis: true,
        tooltip: true,
      },
      {
        title: t('tasks.priority'),
        dataIndex: 'priority',
        slotName: 'priority',
        sortable: {
          sortDirections: ['ascend', 'descend'],
          sorter: true,
        },
        align: 'center',
      },
      {
        title: t('tasks.trigger'),
        dataIndex: 'trigger',
        slotName: 'trigger',
        sortable: {
          sortDirections: ['ascend', 'descend'],
          sorter: true,
        },
        align: 'center',
      },
      {
        title: t('tasks.status'),
        dataIndex: 'status',
        slotName: 'status',
        sortable: {
          sortDirections: ['ascend', 'descend'],
          sorter: true,
        },
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
    ];

    if (props.scope !== 'session') {
      baseColumns.splice(
        2,
        0,
        {
          title: t('tasks.type'),
          dataIndex: 'type',
          slotName: 'type',
          sortable: {
            sortDirections: ['ascend', 'descend'],
            sorter: true,
          },
          align: 'center',
        },
        {
          title: t('robots.name'),
          dataIndex: 'robots',
          slotName: 'robots',
          align: 'center',
        }
      );
    }

    return baseColumns;
  });

  // 获取任务列表查询参数
  const getTasksQueryParams = () => {
    const message = tasksSearchFormModel.value.message.trim();
    const {
      types,
      priorities,
      statuses,
      triggers,
      robots,
      createdTime,
      updatedTime,
    } = tasksSearchFormModel.value;
    const { orderBy, orderType } = tasksTableOrder.value;

    const params: Record<string, any> = {
      project_id: props.selectedSessionItem.id,
      page: tasksTablePagination.value.current,
      size: tasksTablePagination.value.pageSize,
    };

    if (message !== '') {
      params.message = message;
    }
    if (types.length !== 0) {
      params.types = types;
    }
    if (priorities.length !== 0) {
      params.priorities = priorities;
    }
    if (statuses.length !== 0) {
      params.statuses = statuses;
    }
    if (triggers.length !== 0) {
      params.triggers = triggers;
    }
    if (props.scope !== 'session' && robots.length !== 0) {
      params.robots = robots;
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

  // 获取任务列表
  const getTasksItems = async () => {
    tasksTableLoading.value = true;
    try {
      const params = getTasksQueryParams();
      const { data } = await apiGetTasksItems(params);

      tasksItems.value = data.items;
      tasksTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      tasksTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeTasksTablePage = async (page: number) => {
    tasksTableLoading.value = true;
    tasksTablePagination.value.current = page;
    await getTasksItems();
    tasksTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeTasksTablePageSize = async (pageSize: number) => {
    tasksTableLoading.value = true;
    tasksTablePagination.value.pageSize = pageSize;
    await getTasksItems();
    tasksTableLoading.value = false;
  };

  // 切换表格排序
  const changeTasksTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    tasksTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      tasksTableOrder.value.orderBy = dataIndex;
      tasksTableOrder.value.orderType = direction === 'ascend' ? 'asc' : 'desc';
    } else {
      tasksTableOrder.value.orderBy = '';
      tasksTableOrder.value.orderType = '';
    }
    await getTasksItems();
    tasksTableLoading.value = false;
  };

  // 取消任务
  const cancelTasks = async (ids: string[]) => {
    tasksTableLoading.value = true;
    try {
      const params = {
        ids,
      };
      await apiCancelTasks(params);
      await getTasksItems();
      Message.success(t('tasks.cancel.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      tasksTableSelectedKeys.value = [];
      tasksTableLoading.value = false;
    }
  };

  // 重置搜索表单
  const resetTasksSearchFormModel = async () => {
    tasksTableLoading.value = true;
    tasksSearchFormModel.value.message = '';
    tasksSearchFormModel.value.types = [];
    tasksSearchFormModel.value.robots = [];
    tasksSearchFormModel.value.priorities = [];
    tasksSearchFormModel.value.statuses = [];
    tasksSearchFormModel.value.triggers = [];
    tasksSearchFormModel.value.createdTime = [];
    tasksSearchFormModel.value.updatedTime = [];
    await getTasksItems();
    tasksTableLoading.value = false;
  };

  // 更新任务优先级
  const updateTasksPriority = async (id: string) => {
    tasksTableLoading.value = true;
    try {
      const params = {
        id,
        priority: selectedUpdateTasksPriority.value,
      };
      await apiUpdateTasksPriority(params);
      await getTasksItems();
      Message.success(t('common.save.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      tasksTableLoading.value = false;
    }
  };

  onMounted(() => {
    getTasksItems();
  });

  watch(
    () => props.selectedSessionItem.id,
    () => {
      getTasksItems();
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
