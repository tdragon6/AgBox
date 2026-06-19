<template>
  <a-card style="height: 88vh" :title="$t('tasks.scheduler')">
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="schedulerSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="16">
            <a-col :span="6">
              <a-form-item field="name" :label="$t('tasks.name')">
                <a-input
                  v-model="schedulerSearchFormModel.name"
                  :placeholder="$t('tasks.name.placeholder')"
                  allow-clear
                  @keyup.enter="getSchedulerItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="description" :label="$t('tasks.description')">
                <a-input
                  v-model="schedulerSearchFormModel.description"
                  :placeholder="$t('tasks.description.placeholder')"
                  allow-clear
                  @keyup.enter="getSchedulerItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="robot" :label="$t('robots.name')">
                <a-input
                  v-model="schedulerSearchFormModel.robot"
                  :placeholder="$t('robots.name.placeholder')"
                  allow-clear
                  @keyup.enter="getSchedulerItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="createdTime"
                :label="$t('common.time.created')"
              >
                <a-range-picker
                  v-model="schedulerSearchFormModel.createdTime"
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
                field="mountName"
                :label="$t('tasks.scheduler.mountName')"
              >
                <a-input
                  v-model="schedulerSearchFormModel.mountName"
                  :placeholder="$t('tasks.scheduler.mountName.placeholder')"
                  allow-clear
                  @keyup.enter="getSchedulerItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="priorities" :label="$t('tasks.priority')">
                <PrioritySelect
                  v-model="schedulerSearchFormModel.priorities"
                  :multiple="true"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="coordinator" :label="$t('tasks.project')">
                <a-select
                  v-model="schedulerSearchFormModel.coordinator"
                  :options="isBoolOptions"
                  :placeholder="
                    $t('tasks.scheduler.coordinator.select.placeholder')
                  "
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
            <a-col :span="6">
              <a-form-item
                field="updatedTime"
                :label="$t('common.time.updated')"
              >
                <a-range-picker
                  v-model="schedulerSearchFormModel.updatedTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item field="message" :label="$t('tasks.message')">
                <a-input
                  v-model="schedulerSearchFormModel.message"
                  :placeholder="$t('tasks.message.placeholder')"
                  allow-clear
                  @keyup.enter="getSchedulerItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="isPaused"
                :label="$t('tasks.scheduler.isPaused')"
              >
                <a-select
                  v-model="schedulerSearchFormModel.isPaused"
                  :options="isBoolOptions"
                  :placeholder="
                    $t('tasks.scheduler.isPaused.select.placeholder')
                  "
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
            <a-col :span="6">
              <a-form-item
                field="nextRunTime"
                :label="$t('tasks.scheduler.nextRunTime')"
              >
                <a-range-picker
                  v-model="schedulerSearchFormModel.nextRunTime"
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
      <a-divider style="height: 135px" direction="vertical" />
      <a-col :flex="'86px'" style="text-align: right">
        <a-space direction="vertical" :size="18">
          <a-button
            v-debounce
            :loading="schedulerTableLoading"
            type="primary"
            @click="getSchedulerItems"
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            :loading="schedulerTableLoading"
            @click="resetSchedulerSearchFormModel"
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
            @click="
              selectedSchedulerItem = {};
              EditSchedulerModalVisible = true;
            "
          >
            <template #icon>
              <icon-plus />
            </template>
            {{ $t('common.create') }}
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
          @ok="deleteScheduler(schedulerTableSelectedKeys)"
          @ok-loading="schedulerTableLoading"
        >
          <a-button
            :disabled="schedulerTableSelectedKeys.length === 0"
            :loading="schedulerTableLoading"
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
      v-model:selected-keys="schedulerTableSelectedKeys"
      row-key="id"
      :row-selection="{
        type: 'checkbox',
        showCheckedAll: true,
      }"
      :scroll="{ y: 'calc(88vh - 300px)' }"
      :loading="schedulerTableLoading"
      :pagination="schedulerTablePagination"
      :columns="schedulerTableColumns"
      :data="schedulerItems"
      :bordered="false"
      @page-change="changeSchedulerTablePage"
      @page-size-change="changeSchedulerTablePageSize"
      @sorter-change="changeSchedulerTableOrder"
    >
      <template #index="{ rowIndex }">
        {{
          rowIndex +
          1 +
          (schedulerTablePagination.current - 1) *
            schedulerTablePagination.pageSize
        }}
      </template>
      <template #name="{ record }">
        <span :style="{ display: 'flex', alignItems: 'center' }">
          <a-space>
            <a-avatar
              :size="25"
              :style="{
                marginRight: '3px',
                backgroundColor: generateColor(record.name),
              }"
            >
              {{ record.name.charAt(0).toUpperCase() + record.name.charAt(1) }}
            </a-avatar>
            {{ record.name }}
          </a-space>
        </span>
      </template>
      <template #robot="{ record }">
        <a-space v-if="record.coordinator === false">
          <Media
            :style="{
              backgroundColor: 'var(--color-bg-2)',
            }"
            :size="35"
            :url="apiGetRobotsManageAvatarUrl({ name: record.robot })"
            scope="avatar"
          >
          </Media>
          {{ record.robot }}
        </a-space>
        <a-tag
          v-else-if="record.coordinator === true"
          :color="tasksTypeColor[record.robot]"
        >
          {{ $t(coordinatorName[record.robot]) }}
        </a-tag>
      </template>
      <template #mountName="{ record }">
        <a-avatar
          :size="25"
          :style="{
            marginRight: '3px',
            backgroundColor: generateColor(record.mount_name),
          }"
        >
          {{
            record.mount_name.charAt(0).toUpperCase() +
            record.mount_name.charAt(1)
          }}
        </a-avatar>
        {{ record.mount_name }}
      </template>
      <template #priority="{ record }">
        <a-space>
          <a-tag :color="tasksPriorityColor[record.priority]" bordered>
            {{ record.priority }}
          </a-tag>
        </a-space>
      </template>
      <template #coordinator="{ record }">
        <a-badge
          :text="$t(`common.${record.coordinator}`)"
          :status="record.coordinator === true ? 'success' : 'normal'"
        />
      </template>
      <template #isPaused="{ record }">
        <a-badge
          :text="$t(`common.${record.is_paused}`)"
          :status="record.is_paused === true ? 'warning' : 'success'"
        />
      </template>
      <template #time="{ record }">
        <a-tag color="arcoblue">
          {{ record.minute }} {{ record.hour }} {{ record.day }}
          {{ record.month }} {{ record.week }}
        </a-tag>
      </template>
      <template #createdTime="{ record }">
        {{ dayjs(record.created_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #updatedTime="{ record }">
        {{ dayjs(record.updated_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #nextRunTime="{ record }">
        {{
          dayjs(record.next_run_time).isValid()
            ? dayjs(record.next_run_time).format('YYYY-MM-DD HH:mm:ss')
            : '-'
        }}
      </template>
      <template #operations="{ record }">
        <a-button
          v-debounce
          type="text"
          size="small"
          @click="
            selectedSchedulerItem = record;
            EditSchedulerModalVisible = true;
          "
        >
          {{ $t('common.view') }}
        </a-button>
        <a-button
          v-if="record.is_paused === false"
          v-debounce
          type="text"
          size="small"
          status="warning"
          @click="pauseScheduler([record.id])"
        >
          {{ $t('tasks.scheduler.pause') }}
        </a-button>
        <a-button
          v-if="record.is_paused === true"
          v-debounce
          type="text"
          size="small"
          status="success"
          @click="resumeScheduler([record.id])"
        >
          {{ $t('tasks.scheduler.resume') }}
        </a-button>
        <a-popconfirm
          type="warning"
          :content="$t('common.confirm.delete')"
          @ok="deleteScheduler([record.id])"
          @ok-loading="schedulerTableLoading"
        >
          <a-button
            :loading="schedulerTableLoading"
            type="text"
            status="danger"
            size="small"
          >
            {{ $t('common.delete') }}
          </a-button>
        </a-popconfirm>
      </template>
    </a-table>
  </a-card>
  <EditScheduler
    v-if="EditSchedulerModalVisible"
    :selected-scheduler-item="selectedSchedulerItem"
    @close="EditSchedulerModalVisible = false"
    @refresh="getSchedulerItems"
  />
</template>

<script setup lang="ts">
  import { computed, ref, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import { generateColor } from '@marko19907/string-to-color';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    tasksTypeColor,
    coordinatorName,
    tasksPriorityColor,
  } from '@/utils/func';
  import {
    apiGetSchedulerItems,
    apiDeleteScheduler,
    apiPauseScheduler,
    apiResumeScheduler,
  } from '@/api/tasks/scheduler';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import Media from '@/components/media/index.vue';
  import PrioritySelect from '@/components/tasks/tasks-priority-select/index.vue';
  import EditScheduler from './edit-scheduler.vue';

  const { t } = useI18n();

  const schedulerTableLoading = ref(false);

  const EditSchedulerModalVisible = ref(false);

  const schedulerTableSelectedKeys = ref<string[]>([]);
  const selectedSchedulerItem = ref<Record<string, any>>({});
  const schedulerItems = ref<Record<string, any>[]>([]);
  const schedulerTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const schedulerTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const isBoolOptions = computed<Record<string, any>[]>(() => [
    {
      label: t('common.true'),
      value: true,
    },
    {
      label: t('common.false'),
      value: false,
    },
  ]);

  const schedulerSearchFormModel = ref<Record<string, any>>({
    name: '',
    description: '',
    robot: '',
    mountName: '',
    message: '',
    priorities: [],
    coordinator: '',
    isPaused: '',
    createdTime: [],
    updatedTime: [],
    nextRunTime: [],
  });

  const schedulerTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('tasks.name'),
      dataIndex: 'name',
      ellipsis: true,
      tooltip: true,
      slotName: 'name',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('tasks.description'),
      dataIndex: 'description',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('robots.name'),
      dataIndex: 'robot',
      ellipsis: true,
      tooltip: true,
      slotName: 'robot',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('tasks.scheduler.mountName'),
      dataIndex: 'mount_name',
      ellipsis: true,
      tooltip: true,
      slotName: 'mountName',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
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
      title: t('tasks.project'),
      dataIndex: 'coordinator',
      slotName: 'coordinator',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('tasks.scheduler.isPaused'),
      dataIndex: 'is_paused',
      slotName: 'isPaused',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('tasks.scheduler.time'),
      dataIndex: 'time',
      slotName: 'time',
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
      title: t('tasks.scheduler.nextRunTime'),
      dataIndex: 'next_run_time',
      slotName: 'nextRunTime',
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

  // 获取定时任务列表查询参数
  const getSchedulerQueryParams = () => {
    const name = schedulerSearchFormModel.value.name.trim();
    const description = schedulerSearchFormModel.value.description.trim();
    const robot = schedulerSearchFormModel.value.robot.trim();
    const mountName = schedulerSearchFormModel.value.mountName.trim();
    const message = schedulerSearchFormModel.value.message.trim();
    const {
      priorities,
      coordinator,
      isPaused,
      createdTime,
      updatedTime,
      nextRunTime,
    } = schedulerSearchFormModel.value;
    const { orderBy, orderType } = schedulerTableOrder.value;

    const params: Record<string, any> = {
      page: schedulerTablePagination.value.current,
      size: schedulerTablePagination.value.pageSize,
    };

    if (name !== '') {
      params.name = name;
    }
    if (description !== '') {
      params.description = description;
    }
    if (robot !== '') {
      params.robot = robot;
    }
    if (mountName !== '') {
      params.mount_name = mountName;
    }
    if (message !== '') {
      params.message = message;
    }
    if (priorities.length !== 0) {
      params.priorities = priorities;
    }
    if (coordinator !== '') {
      params.coordinator = coordinator;
    }
    if (isPaused !== '') {
      params.is_paused = isPaused;
    }
    if (createdTime.length !== 0) {
      [params.start_created_time, params.end_created_time] = createdTime;
    }
    if (updatedTime.length !== 0) {
      [params.start_updated_time, params.end_updated_time] = updatedTime;
    }
    if (nextRunTime.length !== 0) {
      [params.start_next_run_time, params.end_next_run_time] = nextRunTime;
    }

    if (orderBy !== '' && orderType !== '') {
      params.order_by = orderBy;
      params.order_type = orderType;
    }

    return params;
  };

  // 获取定时任务列表
  const getSchedulerItems = async () => {
    schedulerTableLoading.value = true;
    try {
      const params = getSchedulerQueryParams();
      const { data } = await apiGetSchedulerItems(params);

      schedulerItems.value = data.items;
      schedulerTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeSchedulerTablePage = async (page: number) => {
    schedulerTableLoading.value = true;
    schedulerTablePagination.value.current = page;
    await getSchedulerItems();
    schedulerTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeSchedulerTablePageSize = async (pageSize: number) => {
    schedulerTableLoading.value = true;
    schedulerTablePagination.value.pageSize = pageSize;
    await getSchedulerItems();
    schedulerTableLoading.value = false;
  };

  // 切换表格排序
  const changeSchedulerTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    schedulerTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      schedulerTableOrder.value.orderBy = dataIndex;
      schedulerTableOrder.value.orderType =
        direction === 'ascend' ? 'asc' : 'desc';
    } else {
      schedulerTableOrder.value.orderBy = '';
      schedulerTableOrder.value.orderType = '';
    }
    await getSchedulerItems();
    schedulerTableLoading.value = false;
  };

  // 删除定时任务
  const deleteScheduler = async (ids: string[]) => {
    schedulerTableLoading.value = true;
    try {
      const params = {
        ids,
      };
      await apiDeleteScheduler(params);
      await getSchedulerItems();
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerTableSelectedKeys.value = [];
      schedulerTableLoading.value = false;
    }
  };

  // 重置搜索表单
  const resetSchedulerSearchFormModel = async () => {
    schedulerTableLoading.value = true;
    schedulerSearchFormModel.value.name = '';
    schedulerSearchFormModel.value.description = '';
    schedulerSearchFormModel.value.robot = '';
    schedulerSearchFormModel.value.mountName = '';
    schedulerSearchFormModel.value.message = '';
    schedulerSearchFormModel.value.priorities = [];
    schedulerSearchFormModel.value.coordinator = '';
    schedulerSearchFormModel.value.isPaused = '';
    schedulerSearchFormModel.value.createdTime = [];
    schedulerSearchFormModel.value.updatedTime = [];
    schedulerSearchFormModel.value.nextRunTime = [];
    await getSchedulerItems();
    schedulerTableLoading.value = false;
  };

  // 暂停定时任务
  const pauseScheduler = async (ids: string[]) => {
    schedulerTableLoading.value = true;
    try {
      const params = {
        ids,
      };
      await apiPauseScheduler(params);
      await getSchedulerItems();
      Message.success(t('tasks.scheduler.pause.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerTableLoading.value = false;
    }
  };

  // 恢复定时任务
  const resumeScheduler = async (ids: string[]) => {
    schedulerTableLoading.value = true;
    try {
      const params = {
        ids,
      };
      await apiResumeScheduler(params);
      await getSchedulerItems();
      Message.success(t('tasks.scheduler.resume.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerTableLoading.value = false;
    }
  };

  onMounted(() => {
    getSchedulerItems();
  });
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
