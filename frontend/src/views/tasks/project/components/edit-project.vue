<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    width="50%"
    :ok-loading="projectEditLoading"
    @ok="editProject"
    @cancel="emit('close')"
  >
    <template #title>
      {{
        Object.keys(props.selectedProjectItem).length === 0
          ? $t('common.create')
          : $t('common.edit')
      }}
    </template>
    <a-form :model="projectEditFormModel" auto-label-width label-align="left">
      <a-row :gutter="32">
        <a-col :span="12">
          <a-form-item field="name" :label="$t('tasks.project.name')" required>
            <a-input
              v-model="projectEditFormModel.name"
              :placeholder="$t('tasks.project.name.placeholder')"
              allow-clear
              @keyup.enter="editProject"
            />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item field="robots" :label="$t('tasks.project.robots')">
            <a-avatar-group :size="35" :max-count="5">
              <a-tooltip :content="$t('tasks.project.robots.add')">
                <a-avatar
                  :size="35"
                  :style="{
                    cursor: 'pointer',
                  }"
                  @click="addRobotsModalVisible = true"
                >
                  +
                </a-avatar>
              </a-tooltip>
              <a-tooltip
                v-for="robotItem in projectEditFormModel.robots"
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
                >
                  <template #trigger-icon>
                    <icon-minus
                      @click="
                        projectEditFormModel.robots =
                          projectEditFormModel.robots.filter(
                            (item: string) => item !== robotItem
                          )
                      "
                    />
                  </template>
                </Media>
              </a-tooltip>
            </a-avatar-group>
          </a-form-item>
        </a-col>
        <a-col :span="24">
          <a-form-item
            field="description"
            :label="$t('tasks.project.description')"
            required
          >
            <a-textarea
              v-model="projectEditFormModel.description"
              :placeholder="$t('tasks.project.description.placeholder')"
              :auto-size="{ minRows: 5, maxRows: 5 }"
              allow-clear
            />
          </a-form-item>
        </a-col>
        <a-col
          v-if="Object.keys(props.selectedProjectItem).length !== 0"
          :span="24"
        >
          <a-form-item :label="$t('tasks.project.robots.history')">
            <a-avatar-group
              v-if="props.selectedProjectItem.history_robots.length !== 0"
              :size="35"
              :max-count="5"
            >
              <a-tooltip
                v-for="robotItem in props.selectedProjectItem.history_robots"
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
            <Empty v-else />
          </a-form-item>
        </a-col>
        <a-col
          v-if="Object.keys(props.selectedProjectItem).length !== 0"
          :span="12"
        >
          <a-form-item :label="$t('common.time.created')">
            {{
              dayjs(props.selectedProjectItem.created_time).format(
                'YYYY-MM-DD HH:mm:ss'
              )
            }}
          </a-form-item>
        </a-col>
        <a-col
          v-if="Object.keys(props.selectedProjectItem).length !== 0"
          :span="12"
        >
          <a-form-item :label="$t('common.time.updated')">
            {{
              dayjs(props.selectedProjectItem.updated_time).format(
                'YYYY-MM-DD HH:mm:ss'
              )
            }}
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>
  </a-modal>
  <a-modal
    v-model:visible="addRobotsModalVisible"
    :mask-closable="false"
    :title="$t('tasks.project.robots.add')"
    @ok="
      projectEditFormModel.robots = [
        ...new Set([...projectEditFormModel.robots, ...selectedAddRobotsItems]),
      ];
      selectedAddRobotsItems = [];
    "
  >
    <RobotsSelect
      v-model="selectedAddRobotsItems"
      :multiple="true"
      :selected-project-item="{}"
      scope="robot"
    />
  </a-modal>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import Media from '@/components/media/index.vue';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import { apiCreateProject, apiUpdateProject } from '@/api/tasks/project';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';
  import Empty from '@/components/empty/index.vue';

  const { t } = useI18n();

  const emit = defineEmits<{ close: []; refresh: [string] }>();

  const props = defineProps<{
    selectedProjectItem: Record<string, any>;
  }>();

  const projectEditFormModel = ref<Record<string, any>>({
    name:
      props.selectedProjectItem.name === undefined
        ? ''
        : props.selectedProjectItem.name,
    description:
      props.selectedProjectItem.description === undefined
        ? ''
        : props.selectedProjectItem.description,
    robots:
      props.selectedProjectItem.robots === undefined
        ? []
        : props.selectedProjectItem.robots,
  });

  const projectEditLoading = ref(false);

  const addRobotsModalVisible = ref(false);
  const selectedAddRobotsItems = ref<string[]>([]);

  // 获取编辑项目参数
  const getEditProjectParams = (scope: 'create' | 'update') => {
    const { name, description, robots } = projectEditFormModel.value;
    const params: Record<string, any> = {
      name,
      robots,
    };

    if (description !== '') {
      params.description = description;
    }
    if (robots.length !== 0) {
      params.robots = robots;
    }

    if (scope === 'update') {
      params.id = props.selectedProjectItem.id;
    }
    return params;
  };

  // 创建项目
  const createProject = async () => {
    projectEditLoading.value = true;
    try {
      const params = getEditProjectParams('create');
      const { data } = await apiCreateProject(params);

      Message.success(t('common.create.success'));
      emit('refresh', data.id);
      emit('close');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectEditLoading.value = false;
    }
  };

  // 更新项目
  const updateProject = async () => {
    projectEditLoading.value = true;
    try {
      const params = getEditProjectParams('update');
      await apiUpdateProject(params);

      Message.success(t('common.save.success'));
      emit('refresh', '');
      emit('close');
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectEditLoading.value = false;
    }
  };

  // 编辑项目
  const editProject = async () => {
    if (Object.keys(props.selectedProjectItem).length === 0) {
      createProject();
    } else {
      updateProject();
    }
  };
</script>
