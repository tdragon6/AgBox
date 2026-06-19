<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    width="50%"
    :footer="false"
    @cancel="emit('close')"
  >
    <template #title>
      {{ $t('common.create') }}
    </template>
    <a-space direction="vertical" style="display: flex">
      <a-tabs
        v-if="scope !== 'session'"
        v-model:active-key="tasksTypeTabKey"
        @change="
          if (
            tasksTypeTabKey === 'project' &&
            selectedRobot.startsWith('#') === false
          ) {
            selectedRobot = '#agbox-coordinator-sync';
          }
        "
      >
        <a-tab-pane v-if="scope === 'dashboard'" key="session">
          <template #title>
            {{ $t('tasks.session') }}
          </template>
          <RobotsSessionsDropdown
            v-if="tasksTypeTabKey === 'session'"
            v-model:selected-robot="selectedRobot"
            v-model:selected-session-item="selectedSessionItem"
          />
        </a-tab-pane>
        <a-tab-pane
          v-if="scope === 'dashboard' || scope === 'project'"
          key="project"
        >
          <template #title>
            {{ $t('tasks.project') }}
          </template>
          <ProjectSelect
            v-if="tasksTypeTabKey === 'project'"
            v-model:selected-robot="selectedRobot"
            v-model:selected-project-item="selectedSessionItem"
            :project-options-select="scope === 'dashboard'"
          />
        </a-tab-pane>
      </a-tabs>
      <a-form-item :label="$t('tasks.priority')" required style="width: 30%">
        <PrioritySelect v-model="selectedPriority" :multiple="false" />
      </a-form-item>
      <a-upload
        ref="uploadRef"
        v-model:file-list="pastedImageList"
        :headers="{ Authorization: `Bearer ${getToken()}` }"
        :show-upload-button="false"
        list-type="picture-card"
        name="uf"
        :data="{
          session_id: selectedSessionItem.id,
        }"
        :action="UPLOAD_PASTE_IMAGE_ENDPOINT"
        accept="image/*"
        image-preview
        @success="
          async (fileItem) => {
            const fileName = fileItem.response.data.file_name;
            pastedImageList.push({
              uid: fileName,
              name: fileName,
              url: await apiGetBlobUrl(
                apiGetPasteImageUrl({
                  session_id: selectedSessionItem.id,
                  file_name: fileName,
                })
              ),
            });
            const mentionID = '.paste/' + fileName;
            mentionRef.insertMention({
              id: mentionID,
              label: fileName,
              dataPart: {
                mentionType: '#',
                id: mentionID,
                label: fileName,
              },
            });
          }
        "
        @error="(fileItem) => Message.error(fileItem.response.msg)"
      />
      <MentionInput
        ref="mentionRef"
        :triggers="triggers"
        :placeholder="
          $t('tasks.prompt.at') +
          '\n' +
          $t('tasks.prompt.#') +
          '\n' +
          $t('tasks.prompt.slash') +
          '\n\n' +
          $t('tasks.prompt.enter') +
          '\n' +
          $t('tasks.prompt.newline')
        "
        :style="{ backgroundColor: 'var(--color-bg-2)' }"
        popup-mode="cursor"
        @submit="(dataParts) => createTasks(dataParts)"
        @paste="pasteImage"
      >
        <template #inner-actions="{ submit, clear }">
          <div
            :style="{
              position: 'absolute',
              bottom: '8px',
              left: '20px',
            }"
          >
            <a-space size="medium">
              <a-tooltip :content="$t('tasks.prompt.at')">
                <icon-at class="custom-icon-button" :size="20" />
              </a-tooltip>
              <a-tooltip :content="$t('tasks.prompt.#')">
                <icon class="custom-icon-button" :size="20">
                  <span style="font-size: 20px">#</span>
                </icon>
              </a-tooltip>
              <a-tooltip :content="$t('tasks.prompt.slash')">
                <icon class="custom-icon-button" :size="20">
                  <span style="font-size: 20px">/</span>
                </icon>
              </a-tooltip>
            </a-space>
          </div>
          <div
            :style="{
              position: 'absolute',
              bottom: '8px',
              right: '20px',
            }"
          >
            <a-space size="large">
              <a-space size="medium">
                <a-tooltip :content="$t('tasks.workspaces')">
                  <icon-folder
                    v-debounce
                    class="custom-icon-button"
                    :size="20"
                    @click="openWorkspaces = true"
                  />
                </a-tooltip>
                <a-tooltip :content="$t('tasks.input.clear')">
                  <icon-close-circle
                    v-debounce
                    class="custom-icon-button"
                    :size="20"
                    @click="clear"
                  />
                </a-tooltip>
              </a-space>
              <a-button
                size="small"
                :disabled="mentionRef?.getDataParts().length === 0"
                :loading="createTasksLoading"
                @click="submit"
              >
                <icon-arrow-rise
                  v-debounce
                  class="custom-icon-button"
                  :size="20"
                />
                {{ $t('tasks.send') }}
              </a-button>
            </a-space>
          </div>
        </template>
        <template #item="{ item }">
          <a-space v-if="item.mentionType === '@'">
            <Media
              :style="{
                backgroundColor: 'var(--color-bg-2)',
              }"
              :size="25"
              :url="apiGetRobotsManageAvatarUrl({ name: item.id })"
              scope="avatar"
            />
            {{ item.label }}
          </a-space>
          <a-tooltip
            v-else
            style="z-index: 10000"
            :content="item.id"
            position="top"
          >
            <a-tag color="arcoblue">{{ item.label }}</a-tag>
          </a-tooltip>
        </template>
      </MentionInput>
    </a-space>
    <a-divider />
    <div style="display: flex; justify-content: flex-end">
      <a-space size="large">
        <a-tag
          v-if="selectedRobot !== '' && selectedRobot.startsWith('#') === false"
          color="arcoblue"
        >
          {{ $t('tasks.session') }}
        </a-tag>
        <a-tag
          v-if="selectedRobot !== '' && selectedRobot.startsWith('#') === true"
          color="orangered"
        >
          {{ $t('tasks.project') }}
        </a-tag>
        <a-space
          v-if="selectedRobot !== '' && selectedRobot.startsWith('#') === false"
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
          v-if="selectedRobot !== '' && selectedRobot.startsWith('#') === true"
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
    </div>
    <Files
      v-if="openWorkspaces === true && selectedSessionItem.id !== undefined"
      :name="selectedSessionItem.id"
      scope="workspaces"
      :robot="''"
      @close="openWorkspaces = false"
    />
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message, FileItem } from '@arco-design/web-vue';
  import {
    MentionInput,
    MentionTrigger,
    MentionItem,
    DataPart,
  } from 'mentionly';
  import 'mentionly/style.css';
  import { generateColor } from '@marko19907/string-to-color';
  import {
    apiRunTasks,
    UPLOAD_PASTE_IMAGE_ENDPOINT,
    apiGetPasteImageUrl,
  } from '@/api/tasks/task';
  import { apiGetTreeNodeData } from '@/api/files';
  import Files from '@/components/files/index.vue';
  import PrioritySelect from '@/components/tasks/tasks-priority-select/index.vue';
  import Media from '@/components/media/index.vue';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import apiGetBlobUrl from '@/api/blob';
  import RobotsSessionsDropdown from '@/components/tasks/robots-sessions-dropdown/index.vue';
  import ProjectSelect from '@/components/tasks/project-select/index.vue';
  import { getToken } from '@/utils/auth.js';
  import { tasksTypeColor, coordinatorName } from '@/utils/func.js';

  const { t } = useI18n();

  const props = defineProps<{
    sessionItem: Record<string, any>;
    robot: string;
  }>();

  const emit = defineEmits<{ close: []; refresh: [] }>();

  const createTasksLoading = ref(false);

  const selectedRobot = ref('');
  const selectedSessionItem = ref<Record<string, any>>({});
  const atRobots = ref<string[]>([]);

  const tasksTypeTabKey = ref('');
  const uploadRef = ref();
  const mentionRef = ref();
  const selectedPriority = ref('P3');
  const openWorkspaces = ref(false);
  const pastedImageList = ref<FileItem[]>([]);

  const scope = computed(() => {
    if (props.robot !== '') {
      return props.robot.startsWith('#') ? 'project' : 'session';
    }
    return 'dashboard';
  });

  // 获取 @ 可用数字员工列表
  const getRobotsList = async () => {
    const result: MentionItem[] = [];
    if (scope.value === 'project' || scope.value === 'dashboard') {
      atRobots.value = [];
      selectedSessionItem.value.robots.forEach((item: string) => {
        result.push({
          id: item,
          label: item,
          mentionType: '@',
        });
      });
    }
    return result;
  };

  // 获取 # 可用文件列表
  const getFilesList = async () => {
    // eslint-disable-next-line no-promise-executor-return
    try {
      const params: Record<string, any> = {
        name: selectedSessionItem.value.id,
        scope: 'workspaces',
      };
      const { data } = await apiGetTreeNodeData(params);
      const result: MentionItem[] = [];
      const traverse = (nodes: Record<string, any>[]) => {
        nodes.forEach((item) => {
          if (
            ['.git', '.gitignore', '.worktrees', '.pastes'].includes(
              item.key
            ) === false
          ) {
            result.push({
              id: item.key,
              label: item.title,
              mentionType: '#',
            });
            if (item.children && item.children.length) {
              traverse(item.children);
            }
          }
        });
      };
      traverse(data.children);
      return result;
    } catch (_) {
      return [];
    }
  };

  const triggers: MentionTrigger[] = [
    {
      char: '@',
      items: () => getRobotsList(),
    },
    {
      char: '#',
      items: () => getFilesList(),
    },
    {
      char: '/',
      mode: 'command',
      items: [
        { id: 'clear', label: 'clear', mentionType: '/' },
        // { id: 'submit', label: 'submit', mentionType: '/' },
      ],
      onSelect: (item) => {
        if (item.id === 'clear') {
          mentionRef.value.clear();
        }
        // else if (item.id === 'submit') {
        //   mentionRef.value.submit();
        // }
      },
    },
  ];

  // 粘贴图片
  const pasteImage = (event: ClipboardEvent) => {
    const { clipboardData } = event;
    if (!clipboardData) return;

    const { items } = clipboardData;

    for (let i = 0; i < items.length; i += 1) {
      const item = items[i];
      if (item.type.startsWith('image/')) {
        const file = item.getAsFile();
        if (file) {
          uploadRef.value.upload([file]);
        }
        event.preventDefault();
      }
    }
  };

  // 获取任务提示词
  const getTasksPrompt = (dataParts: DataPart[]) => {
    let prompt = '';
    dataParts.forEach((item) => {
      if (item.type === 'text') {
        prompt += item.text;
      } else if (item.type === 'data') {
        let hint = '';
        if (item.mentionType === '@') {
          hint = 'Please assign this task to the digital employee: ';
        } else {
          hint =
            'Relative file path (based on the current working directory): ';
        }
        prompt += hint + item.id;
      }
    });

    return prompt;
  };

  // 创建任务
  const createTasks = async (dataParts: DataPart[]) => {
    createTasksLoading.value = true;
    try {
      if (dataParts.length === 0) {
        return;
      }

      const params: Record<string, any> = {
        name: selectedRobot.value.startsWith('#')
          ? selectedRobot.value.slice(1)
          : selectedRobot.value,
        session_id: selectedSessionItem.value.id,
        message: getTasksPrompt(dataParts),
        priority: selectedPriority.value,
        coordinator: selectedRobot.value.startsWith('#'),
      };

      await apiRunTasks(params);
      emit('close');
      emit('refresh');
      Message.success(t('common.create.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      createTasksLoading.value = false;
    }
  };

  onMounted(() => {
    if (scope.value !== 'dashboard') {
      selectedSessionItem.value = props.sessionItem;
      selectedRobot.value = props.robot;
      if (scope.value === 'project') {
        tasksTypeTabKey.value = 'project';
      }
    } else {
      tasksTypeTabKey.value = 'session';
    }
  });
</script>

<style scoped>
  :deep(.mentionly-editor) {
    min-height: 240px !important;
    max-height: 240px !important;
    padding-bottom: 48px !important;
  }
</style>
