<template>
  <a-card :bordered="false" size="small">
    <template #title>
      <a-space>
        <icon-file />
        {{ props.filePath }}
        <a-tooltip :content="$t('common.refresh')">
          <icon-refresh
            v-debounce
            class="custom-icon-button"
            @click="readFile"
          />
        </a-tooltip>
      </a-space>
    </template>
    <template #extra>
      <a-button
        v-debounce
        type="outline"
        size="small"
        :loading="editorLoading"
        @click="saveFile"
      >
        {{ $t('common.save') }}
      </a-button>
    </template>
    <a-spin
      :loading="editorLoading"
      style="
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
      "
    >
      <Media
        v-if="fileType === 'image'"
        :style="{}"
        :size="0"
        :url="mediaUrl"
        scope="image"
      />
      <Media
        v-else-if="fileType === 'video'"
        :style="{}"
        :size="0"
        :url="mediaUrl"
        scope="video"
      />
      <vue-monaco-editor
        v-else
        v-model:value="fileContent"
        style="height: 72vh"
        theme="vs-dark"
        :language="getLanguageByExtension()"
        :options="{
          minimap: { enabled: true },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          wordWrap: 'on',
        }"
        @mount="mountEditorCommand"
      />
    </a-spin>
  </a-card>
</template>

<script setup lang="ts">
  import { VueMonacoEditor } from '@guolao/vue-monaco-editor';
  import * as monaco from 'monaco-editor';
  import { ref, onMounted, watch, computed } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import {
    apiReadTreeNodeFile,
    apiSaveTreeNodeFile,
    apiGetFileUrl,
  } from '@/api/files';
  import {
    apiReadRobotsManageRule,
    apiSaveRobotsManageRule,
    apiReadRobotsManageMemory,
    apiSaveRobotsManageMemory,
    apiReadRobotsManageConfig,
    apiSaveRobotsManageConfig,
    apiReadRobotsManageEnv,
    apiSaveRobotsManageEnv,
  } from '@/api/robots/manage';
  import Media from '@/components/media/index.vue';

  const languages = monaco.languages.getLanguages();

  const { t } = useI18n();

  const editorLoading = ref(false);

  const props = defineProps<{
    name: string;
    scope: 'skills' | 'workspaces' | 'rule' | 'memory' | 'config' | 'env';
    filePath: string;
    robot: string;
  }>();

  const fileContent = ref('');
  const fileType = ref<'image' | 'video' | 'file'>('file');

  // 图片或视频URL
  const mediaUrl = computed(() => {
    const params: Record<string, any> = {
      name: props.name,
      scope: props.scope,
      file_path: fileContent.value,
    };
    if (props.robot !== '') {
      params.robot = props.robot;
    }
    return apiGetFileUrl(params);
  });

  // 读取文件
  const readFile = async () => {
    editorLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
      };
      let data = { file_type: 'file', content: '' };

      switch (props.scope) {
        case 'skills':
        case 'workspaces': {
          params.scope = props.scope;
          params.file_path = props.filePath;
          if (props.robot !== '') {
            params.robot = props.robot;
          }
          ({ data } = await apiReadTreeNodeFile(params));
          break;
        }
        case 'rule': {
          ({ data } = await apiReadRobotsManageRule(params));
          break;
        }
        case 'memory': {
          ({ data } = await apiReadRobotsManageMemory(params));
          break;
        }
        case 'config': {
          ({ data } = await apiReadRobotsManageConfig(params));
          break;
        }
        case 'env': {
          ({ data } = await apiReadRobotsManageEnv(params));
          break;
        }
        default: {
          data = { file_type: 'file', content: '' };
          break;
        }
      }
      if (data.file_type === 'file') {
        fileType.value = 'file';
      } else {
        fileType.value = data.file_type as 'image' | 'video';
      }
      fileContent.value = data.content;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      editorLoading.value = false;
    }
  };

  // 保存文件/目录
  const saveFile = async () => {
    editorLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
        content: fileContent.value,
      };
      switch (props.scope) {
        case 'skills':
        case 'workspaces': {
          params.scope = props.scope;
          params.file_path = props.filePath;
          if (props.robot !== '') {
            params.robot = props.robot;
          }
          await apiSaveTreeNodeFile(params);
          break;
        }
        case 'rule': {
          await apiSaveRobotsManageRule(params);
          break;
        }
        case 'memory': {
          await apiSaveRobotsManageMemory(params);
          break;
        }
        case 'config': {
          await apiSaveRobotsManageConfig(params);
          break;
        }
        case 'env': {
          await apiSaveRobotsManageEnv(params);
          break;
        }
        default: {
          break;
        }
      }
      Message.success(t('common.save.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      editorLoading.value = false;
    }
  };

  // 挂载快捷键
  const mountEditorCommand = (monacoEditor: any) => {
    /* eslint-disable no-bitwise */
    monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      if (monacoEditor.hasTextFocus()) {
        saveFile();
      }
    });
  };

  // 根据节点相对路径 key 获取语言
  const getLanguageByExtension = () => {
    const ext = `.${(props.filePath.split('/').pop() as string)
      .split('.')
      .pop()}`;
    const language =
      languages.find((lang) => lang.extensions?.includes(ext as string))?.id ||
      '';
    if (language === undefined) {
      return 'plaintext';
    }
    return language;
  };

  onMounted(() => {
    readFile();
  });

  watch(
    () => props.filePath,
    () => {
      if (props.filePath !== '') {
        readFile();
      }
    }
  );
</script>
