<template>
  <a-spin style="width: 100%" :loading="projectItemsLoading">
    <a-card style="height: 88vh">
      <template #title>
        <a-space>
          {{ $t('tasks.project') }}
          <a-tooltip :content="$t('common.refresh')">
            <icon-refresh
              v-debounce
              class="custom-icon-button"
              @click="getProjectItems"
            />
          </a-tooltip>
        </a-space>
      </template>
      <template #extra>
        <a-space>
          <a-tooltip :content="$t('common.create')">
            <icon-plus
              v-debounce
              class="custom-icon-button"
              @click="
                editProjectItem = {};
                editProjectmodalVisible = true;
              "
            />
          </a-tooltip>
          <a-tooltip :content="$t('common.search')">
            <icon-filter
              v-debounce
              :style="
                JSON.stringify(projectSearchFormModel) !==
                JSON.stringify(defaultProjectSearchFormModel)
                  ? { color: 'var(--color-primary)' }
                  : {}
              "
              class="custom-icon-button"
              @click="searchProjectFormmodalVisible = true"
            />
          </a-tooltip>
        </a-space>
      </template>
      <a-menu
        :selected-keys="
          Object.keys(selectedProjectItem).length !== 0
            ? [selectedProjectItem.id]
            : []
        "
        class="custom-overflow-80vh"
      >
        <Empty v-if="projectItems.length === 0" />
        <a-menu-item
          v-for="item in projectItems"
          v-else
          :key="item.id"
          v-debounce
          @click="selectedProjectItem = item"
        >
          <template #icon>
            <a-avatar
              :size="30"
              :style="{ backgroundColor: generateColor(item.name) }"
            >
              {{ item.name.charAt(0).toUpperCase() + item.name.charAt(1) }}
            </a-avatar>
          </template>
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
              v-debounce
              class="custom-action-icon"
              @click="
                editProjectItem = item;
                editProjectmodalVisible = true;
              "
            />
          </a-tooltip>
          <a-popconfirm
            type="warning"
            :content="$t('common.confirm.delete')"
            @ok="deleteProject(item.id)"
            @ok-loading="projectItemsLoading"
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
  <SearchProjectForm
    v-if="searchProjectFormmodalVisible === true"
    v-model:project-search-form-model="projectSearchFormModel"
    @reset="
      projectSearchFormModel = JSON.parse(
        JSON.stringify(defaultProjectSearchFormModel)
      );
      getProjectItems();
    "
    @refresh="getProjectItems"
    @close="searchProjectFormmodalVisible = false"
  />
  <EditProject
    v-if="editProjectmodalVisible === true"
    :selected-project-item="editProjectItem"
    @refresh="(id) => refreshEditProjectItems(id)"
    @close="editProjectmodalVisible = false"
  />
</template>

<script setup lang="ts">
  import { ref, nextTick, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import Empty from '@/components/empty/index.vue';
  import { generateColor } from '@marko19907/string-to-color';
  import { apiGetProjectItems, apiDeleteProject } from '@/api/tasks/project';
  import { checkTitleOverflow } from '@/utils/func';
  import SearchProjectForm from './search-project-form.vue';
  import EditProject from './edit-project.vue';

  const { t } = useI18n();

  const searchProjectFormmodalVisible = ref(false);
  const editProjectmodalVisible = ref(false);
  const projectItemsLoading = ref(false);

  const editProjectItem = ref<Record<string, any>>({});

  const defaultProjectSearchFormModel = {
    name: '',
    description: '',
    robots: [],
    historyRobots: [],
    createdTime: [],
    updatedTime: [],
  };

  const projectItems = ref<Record<string, any>[]>([]);
  const projectSearchFormModel = ref(
    JSON.parse(JSON.stringify(defaultProjectSearchFormModel))
  );

  const selectedProjectItem = defineModel<Record<string, any>>(
    'selectedProjectItem',
    {
      default: {},
    }
  );

  // 获取项目列表查询参数
  const getProjectQueryParams = () => {
    const name = projectSearchFormModel.value.name.trim();
    const description = projectSearchFormModel.value.description.trim();
    const { robots, historyRobots, createdTime, updatedTime } =
      projectSearchFormModel.value;

    const params: Record<string, any> = {
      page: 0,
    };

    if (name !== '') {
      params.name = name;
    }
    if (description !== '') {
      params.description = description;
    }
    if (robots.length !== 0) {
      params.robots = robots;
    }
    if (historyRobots.length !== 0) {
      params.historyRobrobots = historyRobots;
    }
    if (createdTime.length !== 0) {
      [params.start_created_time, params.end_created_time] = createdTime;
    }
    if (updatedTime.length !== 0) {
      [params.start_updated_time, params.end_updated_time] = updatedTime;
    }

    return params;
  };

  // 获取项目列表
  const getProjectItems = async () => {
    projectItemsLoading.value = true;
    try {
      const params = getProjectQueryParams();
      const { data } = await apiGetProjectItems(params);
      projectItems.value = data.items;

      if (projectItems.value.length !== 0) {
        if (Object.keys(selectedProjectItem.value).length === 0) {
          [selectedProjectItem.value] = projectItems.value;
        } else {
          const nowItem = projectItems.value.find(
            (item) => item.id === selectedProjectItem.value.id
          );
          if (nowItem === undefined) {
            [selectedProjectItem.value] = projectItems.value;
          } else {
            selectedProjectItem.value = nowItem;
          }
        }
      } else {
        selectedProjectItem.value = {};
      }
      await nextTick();
      document
        .querySelector('.custom-overflow-80vh .arco-menu-selected')
        ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectItemsLoading.value = false;
    }
  };

  // 删除项目
  const deleteProject = async (id: string) => {
    projectItemsLoading.value = true;
    try {
      await apiDeleteProject({
        ids: [id],
      });

      projectItems.value = projectItems.value.filter(
        (item: Record<string, any>) => item.id !== id
      );
      if (selectedProjectItem.value.id === id) {
        if (projectItems.value.length !== 0) {
          [selectedProjectItem.value] = projectItems.value;
          await nextTick();
          document
            .querySelector('.custom-overflow-80vh .arco-menu-selected')
            ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
          selectedProjectItem.value = {};
        }
      }
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      projectItemsLoading.value = false;
    }
  };

  // 项目列表 refresh事件
  const refreshEditProjectItems = async (id: string) => {
    await getProjectItems();
    if (id !== '') {
      const updateItem = projectItems.value.find((item) => item.id === id);
      if (updateItem !== undefined) {
        selectedProjectItem.value = updateItem;
      }
    }
    await nextTick();
    document
      .querySelector('.custom-overflow-80vh .arco-menu-selected')
      ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  };

  onMounted(() => {
    getProjectItems();
  });
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
