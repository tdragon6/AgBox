<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    :footer="false"
    width="80%"
    title-align="start"
    @cancel="emit('close')"
  >
    <template #title>
      <a-space>
        {{ props.name }}
        <a-tooltip :content="$t('common.refresh')">
          <icon-refresh
            v-debounce
            class="custom-icon-button"
            @click="getTreeNodeData"
          />
        </a-tooltip>
        <a-tooltip
          v-if="props.scope === 'workspaces'"
          :content="$t('common.export')"
        >
          <icon-download
            v-debounce
            class="custom-icon-button"
            @click="exportWorkspacesDir"
          />
        </a-tooltip>
      </a-space>
    </template>
    <a-row style="height: 80vh">
      <a-col :span="6" class="custom-overflow-80vh">
        <a-spin :loading="treeNodeDataLoading" style="display: block">
          <a-tree
            v-if="treeNodeData.length !== 0"
            v-model:expanded-keys="expandedTreeNodes"
            :selected-keys="selectedTreeNodesKeys"
            :data="treeNodeData"
            draggable
            :allow-drop="allowDrop"
            @select="selectTreeNode"
            @drop="dropTreeNode"
          >
            <template #extra="nodeData">
              <a-dropdown
                :popup-visible="treeNodeDataDropdownVisibleKey === nodeData.key"
                position="br"
                :hide-on-select="false"
                @popup-visible-change="
                  (visible) => {
                    if (!visible) treeNodeDataDropdownVisibleKey = '';
                  }
                "
              >
                <icon-more-vertical
                  style="position: absolute; right: 8px"
                  @click="treeNodeDataDropdownVisibleKey = nodeData.key"
                />
                <template #content>
                  <a-doption
                    v-if="nodeData.isLeaf === false"
                    v-debounce
                    @click="
                      treeNodeDataDropdownVisibleKey = '';
                      openEditModal(nodeData, 'createDir');
                    "
                  >
                    <template #icon> <icon-folder-add /> </template>
                    {{ $t('file.dir.create') }}
                  </a-doption>
                  <a-doption
                    v-if="nodeData.isLeaf === false"
                    v-debounce
                    @click="
                      treeNodeDataDropdownVisibleKey = '';
                      openEditModal(nodeData, 'createFile');
                    "
                  >
                    <template #icon> <icon-plus /> </template>
                    {{ $t('file.file.create') }}
                  </a-doption>
                  <a-doption
                    v-if="nodeData.key !== '.' && nodeData.key !== 'SKILL.md'"
                    v-debounce
                    @click="
                      treeNodeDataDropdownVisibleKey = '';
                      openEditModal(nodeData, 'rename');
                    "
                  >
                    <template #icon> <icon-edit /> </template>
                    {{ $t('common.edit') }}
                  </a-doption>
                  <a-doption
                    v-if="nodeData.isLeaf === true"
                    v-debounce
                    @click="
                      treeNodeDataDropdownVisibleKey = '';
                      downloadFile(nodeData.key);
                    "
                  >
                    <template #icon> <icon-download /> </template>
                    {{ $t('file.download') }}
                  </a-doption>
                  <a-doption
                    v-if="nodeData.isLeaf === false"
                    v-debounce
                    @click="
                      treeNodeDataDropdownVisibleKey = '';
                      uploadFileModalVisible = true;
                      uploadTreeNodeKey = nodeData.key;
                    "
                  >
                    <template #icon> <icon-upload /> </template>
                    {{ $t('file.upload') }}
                  </a-doption>
                  <a-popconfirm
                    v-if="nodeData.key !== '.' && nodeData.key !== 'SKILL.md'"
                    type="warning"
                    :content="`${nodeData.key} ${$t('common.confirm.delete')}`"
                    @ok="deleteTreeNode(nodeData)"
                    @ok-loading="treeNodeDataLoading"
                  >
                    <a-doption>
                      <template #icon> <icon-delete /> </template>
                      {{ $t('common.delete') }}
                    </a-doption>
                  </a-popconfirm>
                </template>
              </a-dropdown>
            </template>
          </a-tree>
          <Empty v-else />
        </a-spin>
      </a-col>
      <a-col :span="1" class="custom-overflow-80vh">
        <a-divider direction="vertical" type="solid" style="height: 100%" />
      </a-col>
      <a-col :span="17" class="custom-overflow-80vh">
        <Editor
          v-if="selectedTreeNodesKeys.length !== 0"
          :name="props.name"
          :scope="props.scope"
          :file-path="selectedTreeNodesKeys[0]"
          :robot="props.robot"
        />
        <Empty v-else />
      </a-col>
    </a-row>
  </a-modal>
  <a-modal
    v-model:visible="treeNodeEditModalVisible"
    :mask-closable="false"
    :title="treeNodeEditModalTitle"
    :ok-loading="treeNodeDataLoading"
    @ok="editTreeNode"
    @cancel="resetEditTreeNode"
  >
    <a-space size="medium" direction="vertical" style="width: 100%">
      <a-typography>
        <a-space size="medium" style="width: 100%">
          <a-typography-text bold>
            {{ $t('file.treeNode.key.current') }}:
          </a-typography-text>
          <a-tag color="arcoblue">{{ editTreeNodeKey }}</a-tag>
        </a-space>
      </a-typography>
      <a-form-item required>
        <a-input
          v-model="editTreeNodeInputValue"
          :placeholder="treeNodeEditModalInputPlaceholder"
          allow-clear
          @keyup.enter="editTreeNode"
        />
      </a-form-item>
    </a-space>
  </a-modal>
  <a-modal
    v-model:visible="uploadFileModalVisible"
    :mask-closable="false"
    :title="$t('file.upload')"
    :footer="false"
    width="60%"
  >
    <a-upload
      :headers="{ Authorization: `Bearer ${getToken()}` }"
      :show-cancel-button="false"
      name="uf"
      :data="(fileItem) => getUploadParams(fileItem.name as string)"
      draggable
      :action="UPLOAD_FILE_ENDPOINT"
      @success="
        async (fileItem) => {
          await getTreeNodeData();
          if (expandedTreeNodes.includes(uploadTreeNodeKey) === false) {
            expandedTreeNodes.push(uploadTreeNodeKey);
          }
          selectedTreeNodesKeys = [
            uploadTreeNodeKey === '.'
              ? (fileItem.name as string)
              : uploadTreeNodeKey + '/' + fileItem.name,
          ];
          uploadTreeNodeKey = '';
          uploadFileModalVisible = false;
          Message.success(t('file.upload.success'));
        }
      "
      @error="(fileItem) => Message.error(fileItem.response.msg)"
    />
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, computed, h, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import { TreeNodeData } from '@arco-design/web-vue/es/tree';
  import Empty from '@/components/empty/index.vue';
  import { IconFile, IconFolder } from '@arco-design/web-vue/es/icon';
  import {
    apiGetTreeNodeData,
    apiCreateTreeNodeFile,
    apiDeleteTreeNodeFile,
    apiRenameTreeNodeFile,
    apiDownloadFile,
    apiDownloadDir,
    UPLOAD_FILE_ENDPOINT,
  } from '@/api/files.js';
  import { getToken } from '@/utils/auth.js';
  import Editor from './editor.vue';

  const { t } = useI18n();

  const props = defineProps<{
    name: string;
    scope: 'skills' | 'workspaces';
    robot: string;
  }>();
  const emit = defineEmits<{ close: [] }>();

  const treeNodeDataLoading = ref(false);

  const treeNodeEditModalVisible = ref(false);
  const uploadFileModalVisible = ref(false);

  const treeNodeData = ref<TreeNodeData[]>([]);
  const selectedTreeNodesKeys = ref<string[]>([]);
  const expandedTreeNodes = ref<string[]>(['.']);
  const treeNodeDataDropdownVisibleKey = ref('');
  const treeNodeEditType = ref<'createDir' | 'createFile' | 'rename'>(
    'createDir'
  );
  const treeNodeEditModalTitle = computed(() => {
    if (treeNodeEditType.value === 'createDir') {
      return t('file.dir.create');
    }
    if (treeNodeEditType.value === 'createFile') {
      return t('file.file.create');
    }
    return t('file.rename');
  });
  const treeNodeEditModalInputPlaceholder = computed(() => {
    if (treeNodeEditType.value === 'createDir') {
      return t('file.dir.placeholder');
    }
    if (treeNodeEditType.value === 'createFile') {
      return t('file.file.placeholder');
    }
    return t('file.rename.placeholder');
  });
  const editTreeNodeKey = ref('');
  const editTreeNodeInputValue = ref('');
  const uploadTreeNodeKey = ref('');

  // 限制脱拽范围
  const allowDrop = ({
    dropNode,
    dropPosition,
  }: {
    dropNode: TreeNodeData;
    dropPosition: number;
  }) => {
    return dropPosition === 0 && dropNode.isLeaf === false;
  };

  // 组装图标
  const processTreeNodeData = (nodes: TreeNodeData[]) => {
    return nodes.map((node) => {
      if (node.isLeaf === true) {
        node.icon = () => h(IconFile);
      } else {
        node.icon = () => h(IconFolder);
      }

      if (Array.isArray(node.children) && node.children.length !== 0) {
        node.children = processTreeNodeData(node.children);
      }

      return node;
    });
  };

  // 获取目录树
  const getTreeNodeData = async () => {
    treeNodeDataLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      const { data } = await apiGetTreeNodeData(params);
      treeNodeData.value = processTreeNodeData([data]);
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      treeNodeDataLoading.value = false;
    }
  };

  // 选择节点
  const selectTreeNode = (keys: (string | number)[], nodeData: any) => {
    if (nodeData.node.isLeaf === true) {
      selectedTreeNodesKeys.value = keys as string[];
    } else if (expandedTreeNodes.value.includes(keys[0] as string) === false) {
      expandedTreeNodes.value.push(keys[0] as string);
    } else {
      expandedTreeNodes.value = expandedTreeNodes.value.filter(
        (item) => item !== (keys[0] as string)
      );
    }
  };

  // 打开编辑模态框
  const openEditModal = (
    nodeData: TreeNodeData,
    type: 'createDir' | 'createFile' | 'rename'
  ) => {
    treeNodeEditType.value = type;
    editTreeNodeKey.value = nodeData.key as string;
    treeNodeEditModalVisible.value = true;
  };

  // 重置编辑模态框
  const resetEditTreeNode = () => {
    editTreeNodeInputValue.value = '';
    editTreeNodeKey.value = '';
    treeNodeEditModalVisible.value = false;
    treeNodeDataLoading.value = false;
  };

  // 创建文件/目录
  const createTreeNode = async (fileType: 'file' | 'dir') => {
    treeNodeDataLoading.value = true;
    try {
      const parentPath = editTreeNodeKey.value;
      const filePath = `${parentPath}/${editTreeNodeInputValue.value}`;
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
        file_path: filePath,
        type: fileType,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiCreateTreeNodeFile(params);
      await getTreeNodeData();
      if (fileType === 'file') {
        selectedTreeNodesKeys.value = [filePath];
      }
      if (expandedTreeNodes.value.includes(parentPath) === false) {
        expandedTreeNodes.value.push(parentPath);
      }
      treeNodeEditModalVisible.value = false;
      Message.success(t('common.create.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      resetEditTreeNode();
    }
  };

  // 重命名文件/目录
  const renameTreeNode = async () => {
    treeNodeDataLoading.value = true;
    try {
      const parentPath = editTreeNodeKey.value
        .split('/')
        .slice(0, -1)
        .join('/');
      const renameFilePath =
        parentPath !== ''
          ? `${parentPath}/${editTreeNodeInputValue.value}`
          : editTreeNodeInputValue.value;
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
        file_path: editTreeNodeKey.value,
        rename_file_path: renameFilePath,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiRenameTreeNodeFile(params);
      await getTreeNodeData();
      if (selectedTreeNodesKeys.value[0] === editTreeNodeKey.value) {
        selectedTreeNodesKeys.value = [renameFilePath];
      }
      treeNodeEditModalVisible.value = false;
      Message.success(t('common.edit.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      resetEditTreeNode();
    }
  };

  // editTreeNode 编辑文件/目录
  const editTreeNode = async () => {
    if (treeNodeEditType.value === 'createDir') {
      createTreeNode('dir');
    } else if (treeNodeEditType.value === 'createFile') {
      createTreeNode('file');
    } else if (treeNodeEditType.value === 'rename') {
      renameTreeNode();
    }
  };

  // 删除文件/目录
  const deleteTreeNode = async (nodeData: TreeNodeData) => {
    treeNodeDataLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
        file_path: nodeData.key,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiDeleteTreeNodeFile(params);
      await getTreeNodeData();
      if (selectedTreeNodesKeys.value[0] === nodeData.key) {
        selectedTreeNodesKeys.value = [];
      }
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      treeNodeDataLoading.value = false;
    }
  };

  // 拖拽文件/目录
  const dropTreeNode = async (dragData: any) => {
    treeNodeDataLoading.value = true;
    try {
      const renameFilePath = `${dragData.dropNode.key}/${dragData.dragNode.key
        .split('/')
        .pop()}`;
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
        file_path: dragData.dragNode.key,
        rename_file_path: renameFilePath,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiRenameTreeNodeFile(params);
      await getTreeNodeData();
      if (selectedTreeNodesKeys.value[0] === dragData.dragNode.key) {
        selectedTreeNodesKeys.value = [renameFilePath];
      }
      Message.success(t('file.move.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      treeNodeDataLoading.value = false;
    }
  };

  // 下载文件
  const downloadFile = async (filePath: string) => {
    treeNodeDataLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
        scope: props.scope,
        file_path: filePath,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiDownloadFile(params);
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      treeNodeDataLoading.value = false;
    }
  };

  // 导出目录
  const exportWorkspacesDir = async () => {
    treeNodeDataLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.name,
        scope: 'workspaces',
      };
      await apiDownloadDir(params);
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      treeNodeDataLoading.value = false;
    }
  };

  // 上传文件
  const getUploadParams = (fileName: string) => {
    const params: Record<string, any> = {
      name: props.name,
      scope: props.scope,
      file_path: `${uploadTreeNodeKey.value}/${fileName}`,
    };
    if (props.robot !== '') {
      params.robot = props.robot;
    }
    return params;
  };

  onMounted(() => {
    getTreeNodeData();
  });
</script>

<style scoped lang="less">
  :deep(.arco-tree-node) {
    .arco-tree-node-title {
      white-space: nowrap;
    }
  }
</style>
