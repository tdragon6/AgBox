<template>
  <a-card :bordered="false" :style="{ height: '75vh' }">
    <template #title>
      <RobotsSelect
        v-if="
          props.robot === '' && selectedTasksOrSessionItem.type !== 'session'
        "
        v-model:selected-robot="selectedRobot"
        style="width: 15%"
        :multiple="false"
        :selected-project-item="selectedTasksOrSessionItem"
        :scope="
          selectedTasksOrSessionItem.type === 'session' ? 'robot' : 'project'
        "
      />
      <a-tag
        v-else-if="props.robot !== '' && props.robot.startsWith('#') === true"
        :color="tasksTypeColor[props.robot.slice(1)]"
      >
        {{ $t(coordinatorName[props.robot.slice(1)]) }}
      </a-tag>
      <a-space v-else>
        <Media
          :style="{
            marginRight: '3px',
            backgroundColor: 'var(--color-bg-2)',
          }"
          :size="25"
          :url="apiGetRobotsManageAvatarUrl({ name: selectedRobot })"
          scope="avatar"
        />
        {{ selectedRobot }}
      </a-space>
    </template>
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="tasksMessagesSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row>
            <a-col :span="12">
              <a-form-item field="roles" :label="$t('tasks.message.role')">
                <a-select
                  v-model="tasksMessagesSearchFormModel.roles"
                  :placeholder="$t('tasks.message.role.placeholder')"
                  multiple
                  allow-clear
                >
                  <a-option
                    v-for="item in tasksMessagesRoleOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{ color: tasksMessagesRoleColor[item.value] }"
                  >
                    <a-tag :color="tasksMessagesRoleColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="12"></a-col>
            <a-col :span="24">
              <a-form-item field="content" :label="$t('tasks.message')">
                <a-input
                  v-model="tasksMessagesSearchFormModel.content"
                  :placeholder="$t('tasks.message.placeholder')"
                  allow-clear
                  @keyup.enter="getTasksMessages"
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
            :loading="tasksMessagesTableLoading"
            type="primary"
            @click="getTasksMessages"
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            :loading="tasksMessagesTableLoading"
            @click="resetTasksMessagesSearchFormModel"
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
      :scroll="{ y: 'calc(75vh - 300px)' }"
      :loading="tasksMessagesTableLoading"
      :pagination="tasksMessagesTablePagination"
      :columns="tasksMessagesTableColumns"
      :data="tasksMessages"
      :bordered="false"
      @page-change="changeTasksMessagesTablePage"
      @page-size-change="changeTasksMessagesTablePageSize"
    >
      <template #index="{ rowIndex }">
        {{
          rowIndex +
          1 +
          (tasksMessagesTablePagination.current - 1) *
            tasksMessagesTablePagination.pageSize
        }}
      </template>
      <template #role="{ record }">
        <a-tag :color="tasksMessagesRoleColor[record.role]" bordered>
          {{ record.role }}
        </a-tag>
      </template>
      <template #timestamp="{ record }">
        {{ dayjs(record.timestamp).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
    </a-table>
  </a-card>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import dayjs from 'dayjs';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    tasksTypeColor,
    coordinatorName,
    tasksMessagesRoleColor,
  } from '@/utils/func';
  import { apiGetTasksMessages } from '@/api/tasks/task';
  import { apiGetRobotsSessionsMessages } from '@/api/tasks/session';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import Media from '@/components/media/index.vue';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';

  const { t } = useI18n();

  const props = defineProps<{
    selectedTasksOrSessionItem: Record<string, any>;
    robot: string;
  }>();

  const tasksMessagesTableLoading = ref(false);

  const tasksMessages = ref<Record<string, any>[]>([]);
  const selectedRobot = ref('');
  const tasksMessagesTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });

  const tasksMessagesRoleOptions = ref([
    {
      value: 'user',
      label: 'user',
    },
    {
      value: 'tool',
      label: 'tool',
    },
    {
      value: 'assistant',
      label: 'assistant',
    },
  ]);

  const tasksMessagesSearchFormModel = ref<Record<string, any>>({
    roles: [],
    content: '',
  });

  const tasksMessagesTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('tasks.message'),
      dataIndex: 'content',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('tasks.message.role'),
      dataIndex: 'role',
      slotName: 'role',
      align: 'center',
    },
    {
      title: t('common.time.created'),
      dataIndex: 'timestamp',
      slotName: 'timestamp',
      align: 'center',
    },
    {
      title: t('tasks.message.reason'),
      dataIndex: 'reasoning',
      ellipsis: true,
      tooltip: true,
    },
  ]);

  // 获取任务消息列表查询参数
  const getTasksMessagesQueryParams = () => {
    const content = tasksMessagesSearchFormModel.value.content.trim();
    const { roles } = tasksMessagesSearchFormModel.value;

    const params: Record<string, any> = {
      page: tasksMessagesTablePagination.value.current,
      size: tasksMessagesTablePagination.value.pageSize,
      name: selectedRobot.value.startsWith('#')
        ? selectedRobot.value.slice(1)
        : selectedRobot.value,
      coordinator: selectedRobot.value.startsWith('#'),
    };

    if (props.selectedTasksOrSessionItem.type !== undefined) {
      params.id = props.selectedTasksOrSessionItem.id;
    } else {
      params.session_id = props.selectedTasksOrSessionItem.id;
    }

    if (content !== '') {
      params.content = content;
    }
    if (roles.length !== 0) {
      params.roles = roles;
    }

    return params;
  };

  // 获取任务消息列表
  const getTasksMessages = async () => {
    tasksMessagesTableLoading.value = true;
    try {
      if (selectedRobot.value === '') {
        return;
      }

      const params = getTasksMessagesQueryParams();

      let resp: Record<string, any> = {};

      if (props.selectedTasksOrSessionItem.type !== undefined) {
        resp = await apiGetTasksMessages(params);
      } else {
        resp = await apiGetRobotsSessionsMessages(params);
      }

      tasksMessages.value = resp.data.items;
      tasksMessagesTablePagination.value.total = resp.data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      tasksMessagesTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeTasksMessagesTablePage = async (page: number) => {
    tasksMessagesTableLoading.value = true;
    tasksMessagesTablePagination.value.current = page;
    await getTasksMessages();
    tasksMessagesTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeTasksMessagesTablePageSize = async (pageSize: number) => {
    tasksMessagesTableLoading.value = true;
    tasksMessagesTablePagination.value.pageSize = pageSize;
    await getTasksMessages();
    tasksMessagesTableLoading.value = false;
  };

  // 重置搜索表单
  const resetTasksMessagesSearchFormModel = async () => {
    tasksMessagesTableLoading.value = true;
    tasksMessagesSearchFormModel.value.roles = [];
    tasksMessagesSearchFormModel.value.content = '';
    await getTasksMessages();
    tasksMessagesTableLoading.value = false;
  };

  onMounted(() => {
    if (
      props.robot === '' &&
      props.selectedTasksOrSessionItem.type === 'session'
    ) {
      [selectedRobot.value] = props.selectedTasksOrSessionItem.robots;
    } else {
      selectedRobot.value = props.robot;
    }
    getTasksMessages();
  });

  watch(
    () => props.robot,
    () => {
      selectedRobot.value = props.robot;
    }
  );

  watch(
    () => selectedRobot.value,
    () => {
      getTasksMessages();
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
