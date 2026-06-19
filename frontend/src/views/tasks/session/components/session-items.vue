<template>
  <a-spin style="width: 100%" :loading="sessionItemsLoading">
    <a-card style="height: 88vh">
      <template #title>
        <a-space>
          {{ $t('tasks.session') }}
          <a-tooltip :content="$t('common.refresh')">
            <icon-refresh
              v-debounce
              class="custom-icon-button"
              @click="getSessionItems"
            />
          </a-tooltip>
        </a-space>
      </template>
      <template #extra>
        <a-tooltip v-if="selectedRobot !== ''" :content="$t('common.create')">
          <icon-plus
            v-debounce
            class="custom-icon-button"
            @click="createSession"
          />
        </a-tooltip>
      </template>
      <a-menu
        :selected-keys="
          Object.keys(selectedSessionItem).length !== 0
            ? [selectedSessionItem.id]
            : []
        "
        class="custom-overflow-80vh"
      >
        <RobotsSelect
          v-model:selected-robot="selectedRobot"
          :multiple="false"
          :selected-project-item="{}"
          scope="robot"
        />
        <a-divider v-if="selectedRobot !== ''" />
        <a-input
          v-if="selectedRobot !== ''"
          v-model="sessionSearchName"
          size="small"
          :placeholder="$t('tasks.session.name.placeholder')"
          allow-clear
          @keyup.enter="getSessionItems"
        >
          <template #prefix>
            <icon-search />
          </template>
        </a-input>
        <a-divider v-if="selectedRobot !== ''" />
        <Empty v-if="sessionItems.length === 0" />
        <a-menu-item
          v-for="item in sessionItems"
          v-else
          :key="item.id"
          v-debounce
          @click="selectedSessionItem = item"
        >
          <template #icon>
            <a-avatar
              :size="30"
              :style="{ backgroundColor: generateColor(item.name) }"
            >
              {{ item.name.charAt(0).toUpperCase() + item.name.charAt(1) }}
            </a-avatar>
          </template>
          <a-input
            v-if="item.input === true"
            v-model="item.name"
            allow-clear
            @keyup.enter="renameSession(item)"
            @blur="renameSession(item)"
            @keyup.esc="resetRenameSession(item)"
            @click.stop
          />
          <a-tooltip v-if="item.overflow === true" :content="item.name">
            <span
              class="custom-ellipsis"
              @mouseenter="checkTitleOverflow($event, item)"
            >
              {{ item.name }}
            </span>
          </a-tooltip>
          <span
            v-else
            class="custom-ellipsis"
            @mouseenter="checkTitleOverflow($event, item)"
          >
            {{ item.name }}
          </span>
          <a-tooltip :content="$t('common.edit')" @click.stop>
            <icon-edit
              v-if="item.input === false"
              v-debounce
              class="custom-action-icon"
              @click="
                switchRenameInput(
                  item,
                  '.custom-overflow-80vh .arco-menu-item input'
                )
              "
            />
          </a-tooltip>
          <a-popconfirm
            type="warning"
            :content="$t('common.confirm.delete')"
            @ok="deleteSession(item.id)"
            @ok-loading="sessionItemsLoading"
            @click.stop
          >
            <a-tooltip :content="$t('common.delete')">
              <icon-delete class="custom-action-icon" />
            </a-tooltip>
          </a-popconfirm>
        </a-menu-item>
      </a-menu>
    </a-card>
  </a-spin>
</template>

<script setup lang="ts">
  import { ref, nextTick, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import Empty from '@/components/empty/index.vue';
  import { generateColor } from '@marko19907/string-to-color';
  import {
    apiGetRobotsSessions,
    apiRenameRobotsSessions,
    apiCreateRobotsSessions,
    apiDeleteRobotsSessions,
  } from '@/api/tasks/session';
  import { checkTitleOverflow, switchRenameInput } from '@/utils/func';
  import RobotsSelect from '@/components/robots/robots-select/index.vue';

  const { t } = useI18n();

  const sessionItemsLoading = ref(false);

  const sessionItems = ref<Record<string, any>[]>([]);
  const sessionSearchName = ref('');

  const selectedSessionItem = defineModel<Record<string, any>>(
    'selectedSessionItem',
    {
      default: {},
    }
  );
  const selectedRobot = defineModel<string>('selectedRobot', {
    default: '',
  });

  // 创建会话
  const createSession = async () => {
    sessionItemsLoading.value = true;
    try {
      const { data } = await apiCreateRobotsSessions({
        names: [selectedRobot.value],
      });

      const item = {
        id: data.session_id,
        name: data.session_id,
        input: false,
        oriName: data.session_id,
        inputTokens: 0,
        outputTokens: 0,
        cacheReadTokens: 0,
        cacheWriteTokens: 0,
        reasoningTokens: 0,
        estimatedCostUsd: 0,
        actualCostUsd: 0,
      };

      sessionItems.value.push(item);

      selectedSessionItem.value = item;

      await nextTick();
      document
        .querySelector('.custom-overflow-80vh .arco-menu-selected')
        ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });

      Message.success(t('common.create.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      sessionItemsLoading.value = false;
    }
  };

  // 获取会话列表
  const getSessionItems = async () => {
    sessionItemsLoading.value = true;
    try {
      if (selectedRobot.value === '') {
        sessionItems.value = [];
        return;
      }

      const params: Record<string, any> = {
        name: selectedRobot.value,
        page: 0,
      };

      if (sessionSearchName.value !== '') {
        params.title = sessionSearchName.value;
      }

      const { data } = await apiGetRobotsSessions(params);

      sessionItems.value = [];
      data.forEach((item: Record<string, any>) => {
        sessionItems.value.push({
          id: item.id,
          name: item.title,
          input: false,
          oriName: item.title,
          inputTokens: item.input_tokens,
          outputTokens: item.output_tokens,
          cacheReadTokens: item.cache_read_tokens,
          cacheWriteTokens: item.cache_write_tokens,
          reasoningTokens: item.reasoning_tokens,
          estimatedCostUsd: item.estimated_cost_usd,
          actualCostUsd: item.actual_cost_usd,
        });
      });

      if (sessionItems.value.length !== 0) {
        if (Object.keys(selectedSessionItem.value).length === 0) {
          [selectedSessionItem.value] = sessionItems.value;
        } else {
          const nowItem = sessionItems.value.find(
            (item) => item.id === selectedSessionItem.value.id
          );
          if (nowItem === undefined) {
            [selectedSessionItem.value] = sessionItems.value;
          } else {
            selectedSessionItem.value = nowItem;
          }
        }
      } else {
        selectedSessionItem.value = {};
      }
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      sessionItemsLoading.value = false;
    }
  };

  const resetRenameSession = (item: Record<string, any>) => {
    item.name = item.oriName;
    item.input = false;
  };

  // 重命名会话
  const renameSession = async (item: Record<string, any>) => {
    sessionItemsLoading.value = true;
    try {
      // esc 取消重命名时捕获 blur 事件不进行请求
      if (item.input === false) {
        return;
      }

      if (item.name === item.oriName) {
        item.input = false;
        return;
      }

      await apiRenameRobotsSessions({
        name: selectedRobot.value,
        session_id: item.id,
        title: item.name,
      });

      item.oriName = item.name;
      item.input = false;

      if (selectedSessionItem.value.id === item.id) {
        selectedSessionItem.value = item;
      }
      Message.success(t('common.edit.success'));
    } catch (_) {
      resetRenameSession(item);
    } finally {
      sessionItemsLoading.value = false;
    }
  };

  // 删除会话
  const deleteSession = async (id: string) => {
    sessionItemsLoading.value = true;
    try {
      await apiDeleteRobotsSessions({
        name: selectedRobot.value,
        session_ids: [id],
      });

      sessionItems.value = sessionItems.value.filter(
        (item: Record<string, any>) => item.id !== id
      );
      if (selectedSessionItem.value.id === id) {
        if (sessionItems.value.length !== 0) {
          [selectedSessionItem.value] = sessionItems.value;
          await nextTick();
          document
            .querySelector('.-80vh .arco-menu-selected')
            ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
          selectedSessionItem.value = {};
        }
      }
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      sessionItemsLoading.value = false;
    }
  };

  watch(
    () => selectedRobot.value,
    () => getSessionItems()
  );
</script>

<style scoped lang="less">
  :deep(.arco-menu-title .arco-trigger) {
    display: flex;
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }

  :deep(.arco-menu-title) {
    display: flex;
    align-items: center;
  }

  :deep(.arco-menu-item:hover) .custom-action-icon {
    opacity: 1;
  }
</style>
