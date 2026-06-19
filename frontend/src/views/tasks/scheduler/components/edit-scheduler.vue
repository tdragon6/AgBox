<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    width="50%"
    :ok-loading="schedulerEditLoading"
    @ok="editScheduler"
    @cancel="emit('close')"
  >
    <template #title>
      {{
        Object.keys(props.selectedSchedulerItem).length === 0
          ? $t('common.create')
          : $t('common.edit')
      }}
    </template>
    <a-form :model="schedulerEditFormModel" auto-label-width label-align="left">
      <a-row :gutter="32">
        <a-col :span="12">
          <a-form-item field="name" :label="$t('tasks.name')" required>
            <a-input
              v-model="schedulerEditFormModel.name"
              :placeholder="$t('tasks.name.placeholder')"
              allow-clear
              @keyup.enter="editScheduler"
            />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item
            field="description"
            :label="$t('tasks.description')"
            required
          >
            <a-input
              v-model="schedulerEditFormModel.description"
              :placeholder="$t('tasks.description.placeholder')"
              allow-clear
              @keyup.enter="editScheduler"
            />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item field="priority" :label="$t('tasks.priority')" required>
            <PrioritySelect
              v-model="schedulerEditFormModel.priority"
              :multiple="false"
            />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item
            field="time"
            :label="$t('tasks.scheduler.time')"
            required
          >
            <a-input
              v-model="schedulerEditFormModel.time"
              :placeholder="$t('tasks.scheduler.time.placeholder')"
              allow-clear
              @keyup.enter="editScheduler"
            />
          </a-form-item>
        </a-col>
        <a-col :span="24">
          <a-form-item field="message" :label="$t('tasks.message')" required>
            <a-input
              v-model="schedulerEditFormModel.message"
              :placeholder="$t('tasks.message.placeholder')"
              allow-clear
              @keyup.enter="editScheduler"
            />
          </a-form-item>
        </a-col>
        <a-col :span="8">
          <a-form-item :label="$t('tasks.scheduler.mountName')" required>
            <a-space
              v-if="
                selectedRobot !== '' &&
                Object.keys(selectedSessionItem).length !== 0
              "
              size="large"
            >
              <a-tag
                v-if="
                  selectedRobot !== '' &&
                  selectedRobot.startsWith('#') === false
                "
                color="arcoblue"
              >
                {{ $t('tasks.session') }}
              </a-tag>
              <a-tag
                v-if="
                  selectedRobot !== '' && selectedRobot.startsWith('#') === true
                "
                color="orangered"
              >
                {{ $t('tasks.project') }}
              </a-tag>
              <a-space
                v-if="
                  selectedRobot !== '' &&
                  selectedRobot.startsWith('#') === false
                "
              >
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
              <a-tag
                v-if="
                  selectedRobot !== '' && selectedRobot.startsWith('#') === true
                "
                :color="tasksTypeColor[selectedRobot.slice(1)]"
              >
                {{ $t(coordinatorName[selectedRobot.slice(1)]) }}
              </a-tag>
              <a-space
                v-if="
                  selectedSessionItem.title !== undefined ||
                  selectedSessionItem.name !== undefined
                "
              >
                <a-avatar
                  :size="20"
                  :style="{
                    backgroundColor: generateColor(
                      selectedSessionItem.title === undefined
                        ? selectedSessionItem.name
                        : selectedSessionItem.title
                    ),
                  }"
                >
                  {{
                    selectedSessionItem.title === undefined
                      ? selectedSessionItem.name.charAt(0).toUpperCase() +
                        selectedSessionItem.name.charAt(1)
                      : selectedSessionItem.title.charAt(0).toUpperCase() +
                        selectedSessionItem.title.charAt(1)
                  }}
                </a-avatar>
                {{
                  selectedSessionItem.title === undefined
                    ? selectedSessionItem.name
                    : selectedSessionItem.title
                }}
              </a-space>
            </a-space>
            <Empty v-else />
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>
    <a-tabs
      v-model:active-key="schedulerMountTypeTabKey"
      @change="
        if (
          schedulerMountTypeTabKey === 'project' &&
          selectedRobot.startsWith('#') === false
        ) {
          selectedRobot = '#agbox-coordinator-sync';
        }
      "
    >
      <a-tab-pane key="session">
        <template #title>
          {{ $t('tasks.session') }}
        </template>
        <RobotsSessionsDropdown
          v-if="schedulerMountTypeTabKey === 'session'"
          v-model:selected-robot="selectedRobot"
          v-model:selected-session-item="selectedSessionItem"
        />
      </a-tab-pane>
      <a-tab-pane key="project">
        <template #title>
          {{ $t('tasks.project') }}
        </template>
        <ProjectSelect
          v-if="schedulerMountTypeTabKey === 'project'"
          v-model:selected-robot="selectedRobot"
          v-model:selected-project-item="selectedSessionItem"
          :project-options-select="true"
        />
      </a-tab-pane>
    </a-tabs>
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import {
    apiCreateScheduler,
    apiUpdateScheduler,
  } from '@/api/tasks/scheduler';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import { generateColor } from '@marko19907/string-to-color';
  import RobotsSessionsDropdown from '@/components/tasks/robots-sessions-dropdown/index.vue';
  import ProjectSelect from '@/components/tasks/project-select/index.vue';
  import PrioritySelect from '@/components/tasks/tasks-priority-select/index.vue';
  import Empty from '@/components/empty/index.vue';
  import Media from '@/components/media/index.vue';
  import { tasksTypeColor, coordinatorName } from '@/utils/func';

  const { t } = useI18n();

  const emit = defineEmits<{ close: []; refresh: [] }>();

  const props = defineProps<{
    selectedSchedulerItem: Record<string, any>;
  }>();

  const schedulerMountTypeTabKey = ref('session');
  const selectedRobot = ref('');
  const selectedSessionItem = ref<Record<string, any>>({});

  const schedulerEditFormModel = ref<Record<string, any>>({
    name:
      props.selectedSchedulerItem.name === undefined
        ? ''
        : props.selectedSchedulerItem.name,
    description:
      props.selectedSchedulerItem.description === undefined
        ? ''
        : props.selectedSchedulerItem.description,
    message:
      props.selectedSchedulerItem.message === undefined
        ? []
        : props.selectedSchedulerItem.message,
    priority:
      props.selectedSchedulerItem.priority === undefined
        ? 'P3'
        : props.selectedSchedulerItem.priority,
    time:
      props.selectedSchedulerItem.minute === undefined ||
      props.selectedSchedulerItem.hour === undefined ||
      props.selectedSchedulerItem.day === undefined ||
      props.selectedSchedulerItem.week === undefined ||
      props.selectedSchedulerItem.month === undefined
        ? ''
        : `${props.selectedSchedulerItem.minute} ${props.selectedSchedulerItem.hour} ${props.selectedSchedulerItem.day} ${props.selectedSchedulerItem.month} ${props.selectedSchedulerItem.week}`,
  });

  const schedulerEditLoading = ref(false);

  // 获取编辑定时任务参数
  const getEditSchedulerParams = (scope: 'create' | 'update') => {
    const [minute, hour, day, month, week] =
      schedulerEditFormModel.value.time.split(' ');
    const params: Record<string, any> = {
      minute,
      hour,
      day,
      week,
      month,
      name: schedulerEditFormModel.value.name,
      description: schedulerEditFormModel.value.description,
      robot: selectedRobot.value.startsWith('#')
        ? selectedRobot.value.slice(1)
        : selectedRobot.value,
      project_id: selectedSessionItem.value.id,
      message: schedulerEditFormModel.value.message,
      priority: schedulerEditFormModel.value.priority,
    };
    if (selectedRobot.value.startsWith('#')) {
      params.coordinator = true;
    }
    if (scope === 'update') {
      params.id = props.selectedSchedulerItem.id;
    }
    return params;
  };

  // 创建定时任务
  const createScheduler = async () => {
    schedulerEditLoading.value = true;
    try {
      const params = getEditSchedulerParams('create');
      await apiCreateScheduler(params);

      Message.success(t('common.create.success'));
      emit('refresh');
      emit('close');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerEditLoading.value = false;
    }
  };

  // 更新定时任务
  const updateScheduler = async () => {
    schedulerEditLoading.value = true;
    try {
      const params = getEditSchedulerParams('update');
      await apiUpdateScheduler(params);

      Message.success(t('common.save.success'));
      emit('refresh');
      emit('close');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      schedulerEditLoading.value = false;
    }
  };

  // 编辑定时任务
  const editScheduler = async () => {
    if (Object.keys(props.selectedSchedulerItem).length === 0) {
      createScheduler();
    } else {
      updateScheduler();
    }
  };

  onMounted(() => {
    if (Object.keys(props.selectedSchedulerItem).length !== 0) {
      selectedRobot.value =
        props.selectedSchedulerItem.coordinator === true
          ? `#${props.selectedSchedulerItem.robot}`
          : props.selectedSchedulerItem.robot;
      selectedSessionItem.value = {
        id: props.selectedSchedulerItem.project_id,
        title: props.selectedSchedulerItem.mount_name,
      };
    }
  });
</script>
