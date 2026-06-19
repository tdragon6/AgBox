<template>
  <a-spin style="width: 100%" :loading="categoryItemsLoading">
    <a-card style="height: 88vh">
      <template #title>
        {{ $t('skills.category') }}
        <a-tooltip :content="$t('common.refresh')">
          <icon-refresh
            v-debounce
            class="custom-icon-button"
            @click="getSkillsCategoryItems"
          />
        </a-tooltip>
      </template>
      <template #extra>
        <a-tooltip :content="$t('common.create')">
          <icon-plus
            v-debounce
            class="custom-icon-button"
            @click="createCategoryModalVisible = true"
          />
        </a-tooltip>
      </template>
      <a-menu
        v-model:selected-keys="selectedCategoryItems"
        class="custom-overflow-80vh"
      >
        <a-menu-item key="#default">
          <template #icon>
            <a-avatar
              :size="30"
              :style="{ backgroundColor: generateColor('#') }"
            >
              #
            </a-avatar>
          </template>
          <span>default</span>
        </a-menu-item>
        <a-divider />
        <Empty v-if="categoryItems.length === 0" />
        <a-menu-item v-for="item in categoryItems" v-else :key="item.id">
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
            @keyup.enter="renameSkillsCategory(item)"
            @blur="renameSkillsCategory(item)"
            @keyup.esc="resetRenameSkillsCategory(item)"
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
          <div style="width: 20%"></div>
          <a-tooltip :content="$t('common.edit')" @click.stop>
            <icon-edit
              v-if="item.input === false"
              v-debounce
              class="custom-action-icon"
              @click="switchRenameInput(item, '.custom-overflow-80vh input')"
            />
          </a-tooltip>
          <a-popconfirm
            type="warning"
            :content="$t('common.confirm.delete')"
            @ok="deleteSkillsCategory(item.id)"
            @ok-loading="categoryItemsLoading"
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
  <a-modal
    v-model:visible="createCategoryModalVisible"
    :mask-closable="false"
    :title="$t('common.create')"
    :ok-loading="categoryCreateLoading"
    @ok="createSkillsCategory"
    @cancel="createCategoryName = ''"
  >
    <a-form-item required>
      <a-input
        v-model="createCategoryName"
        :placeholder="$t('skills.category.placeholder')"
        allow-clear
        @keyup.enter="createSkillsCategory"
      />
    </a-form-item>
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, onMounted, nextTick } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import Empty from '@/components/empty/index.vue';
  import { generateColor } from '@marko19907/string-to-color';
  import {
    apiCreateSkillsCategory,
    apiGetSkillsCategoryItems,
    apiRenameSkillsCategory,
    apiDeleteSkillsCategory,
  } from '@/api/skills';
  import { checkTitleOverflow, switchRenameInput } from '@/utils/func';

  const { t } = useI18n();

  const categoryItemsLoading = ref(false);
  const categoryCreateLoading = ref(false);

  const createCategoryModalVisible = ref(false);
  const categoryItems = ref<Record<string, any>[]>([]);
  const createCategoryName = ref('');

  const selectedCategoryItems = defineModel<string[]>('selectedCategoryItems', {
    default: ['#default'],
  });

  const props = defineProps<{ robot: string }>();

  // 创建技能分类
  const createSkillsCategory = async () => {
    categoryCreateLoading.value = true;
    try {
      const categoryName = createCategoryName.value.trim();
      const params: Record<string, any> = {
        category: categoryName,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiCreateSkillsCategory(params);

      categoryItems.value.push({
        id: categoryName,
        name: categoryName,
        input: false,
        oriName: categoryName,
      });

      selectedCategoryItems.value = [categoryName];

      await nextTick();
      document
        .querySelector('.custom-overflow-80vh .arco-menu-selected')
        ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });

      createCategoryName.value = '';
      createCategoryModalVisible.value = false;
      Message.success(t('common.create.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      categoryCreateLoading.value = false;
    }
  };

  // 获取技能分类列表
  const getSkillsCategoryItems = async () => {
    categoryItemsLoading.value = true;
    try {
      const params: Record<string, any> = {};
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      const { data } = await apiGetSkillsCategoryItems(params);
      categoryItems.value = [];
      data.forEach((item: string) => {
        categoryItems.value.push({
          id: item,
          name: item,
          input: false,
          oriName: item,
        });
      });
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      categoryItemsLoading.value = false;
    }
  };

  const resetRenameSkillsCategory = (item: Record<string, any>) => {
    item.name = item.oriName;
    item.input = false;
  };

  // 重命名技能分类
  const renameSkillsCategory = async (item: Record<string, any>) => {
    categoryItemsLoading.value = true;
    try {
      // esc 取消重命名时捕获 blur 事件不进行请求
      if (item.input === false) {
        return;
      }

      if (item.name === item.oriName) {
        item.input = false;
        return;
      }

      const params: Record<string, any> = {
        old_category: item.id,
        new_category: item.name,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiRenameSkillsCategory(params);

      if (selectedCategoryItems.value[0] === item.id) {
        selectedCategoryItems.value = [item.name];
      }

      item.id = item.name;
      item.oriName = item.name;
      item.input = false;

      Message.success(t('common.edit.success'));
    } catch (_) {
      resetRenameSkillsCategory(item);
    } finally {
      categoryItemsLoading.value = false;
    }
  };

  // 删除技能分类
  const deleteSkillsCategory = async (id: string) => {
    categoryItemsLoading.value = true;
    try {
      const params: Record<string, any> = {
        category: id,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiDeleteSkillsCategory(params);

      categoryItems.value = categoryItems.value.filter(
        (item: Record<string, any>) => item.id !== id
      );
      if (selectedCategoryItems.value[0] === id) {
        selectedCategoryItems.value = ['#default'];

        await nextTick();
        document
          .querySelector('.custom-overflow-80vh .arco-menu-selected')
          ?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      categoryItemsLoading.value = false;
    }
  };

  onMounted(() => {
    getSkillsCategoryItems();
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
