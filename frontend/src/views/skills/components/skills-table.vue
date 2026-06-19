<template>
  <div class="container">
    <a-card style="height: 88vh" :title="$t('skills')">
      <a-row>
        <a-col :flex="1">
          <a-form
            :model="skillsSearchFormModel"
            auto-label-width
            label-align="left"
          >
            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-item field="name" :label="$t('skills.name')">
                  <a-input
                    v-model="skillsSearchFormModel.name"
                    :placeholder="$t('skills.name.placeholder')"
                    allow-clear
                    @keyup.enter="getSkillsItems"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item field="isScript" :label="$t('skills.isScript')">
                  <a-select
                    v-model="skillsSearchFormModel.isScript"
                    :options="isScriptOptions"
                    :placeholder="$t('skills.isScript.select.placeholder')"
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
              <a-col :span="24">
                <a-form-item
                  field="description"
                  :label="$t('skills.description')"
                >
                  <a-input
                    v-model="skillsSearchFormModel.description"
                    :placeholder="$t('skills.description.placeholder')"
                    allow-clear
                    @keyup.enter="getSkillsItems"
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
              :loading="skillsTableLoading"
              type="primary"
              @click="getSkillsItems"
            >
              <template #icon>
                <icon-search />
              </template>
              {{ $t('common.search') }}
            </a-button>
            <a-button
              v-debounce
              :loading="skillsTableLoading"
              @click="resetSkillsSearchFormModel"
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
                props.robot !== ''
                  ? (robotsImportSkillsModalVisible = true)
                  : (importSkillsModalVisible = true)
              "
            >
              <template #icon>
                <icon-download />
              </template>
              {{
                props.robot !== '' ? $t('skills.import') : $t('import.skills')
              }}
            </a-button>
            <a-button
              v-if="props.robot === ''"
              v-debounce
              size="small"
              type="primary"
              status="normal"
              @click="skillsMarketTableVisible = true"
            >
              <template #icon>
                <icon-cloud-download />
              </template>
              {{ $t('skills.market') }}
            </a-button>
          </a-space>
        </a-col>
        <a-col
          :span="12"
          style="display: flex; align-items: center; justify-content: end"
        >
          <a-space>
            <a-button
              v-if="props.robotImport === true && props.robot === ''"
              v-debounce
              :disabled="skillsTableSelectedKeys.length === 0"
              :loading="skillsTableLoading"
              size="small"
              type="outline"
              status="normal"
              @click="robotImportSkills(skillsTableSelectedKeys)"
            >
              <template #icon>
                <icon-download />
              </template>
              {{ $t('skills.import.batch') }}
            </a-button>
            <a-popconfirm
              type="warning"
              :content="$t('common.confirm.delete')"
              @ok="deleteSkills(skillsTableSelectedKeys)"
              @ok-loading="skillsTableLoading"
            >
              <a-button
                :disabled="skillsTableSelectedKeys.length === 0"
                :loading="skillsTableLoading"
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
          </a-space>
        </a-col>
      </a-row>
      <a-table
        v-model:selected-keys="skillsTableSelectedKeys"
        row-key="name"
        :row-selection="{
          type: 'checkbox',
          showCheckedAll: true,
        }"
        :scroll="{ y: 'calc(88vh - 300px)' }"
        :loading="skillsTableLoading"
        :pagination="skillsTablePagination"
        :columns="skillsTableColumns"
        :data="skillsItems"
        :bordered="false"
        @page-change="changeSkillsTablePage"
        @page-size-change="changeSkillsTablePageSize"
        @sorter-change="changeSkillsTableOrder"
      >
        <template #index="{ rowIndex }">
          {{
            rowIndex +
            1 +
            (skillsTablePagination.current - 1) * skillsTablePagination.pageSize
          }}
        </template>
        <template #name="{ record }">
          <a-tag color="orangered" bordered>
            <template #icon> <icon-tool /> </template>
            {{ record.name }}
          </a-tag>
        </template>
        <template #isScript="{ record }">
          <a-badge
            :text="$t(`common.${record.is_script}`)"
            :status="record.is_script === true ? 'success' : 'normal'"
          />
        </template>
        <template #operations="{ record }">
          <a-button
            v-debounce
            type="text"
            size="small"
            @click="selectedSkillsName = record.name"
          >
            {{ $t('common.view') }}
          </a-button>
          <a-popconfirm
            type="warning"
            :content="$t('common.confirm.delete')"
            @ok="deleteSkills([record.name])"
            @ok-loading="skillsTableLoading"
          >
            <a-button
              :loading="skillsTableLoading"
              type="text"
              status="danger"
              size="small"
            >
              {{ $t('common.delete') }}
            </a-button>
          </a-popconfirm>
          <a-button
            v-debounce
            type="text"
            status="normal"
            size="small"
            @click="exportSkills(record.name)"
          >
            <template #icon>
              <icon-share-internal />
            </template>
            {{ $t('common.export') }}
          </a-button>
          <a-button
            v-if="props.robotImport && props.robot === ''"
            v-debounce
            type="text"
            status="normal"
            size="small"
            @click="robotImportSkills([record.name])"
          >
            <template #icon>
              <icon-download />
            </template>
            {{ $t('common.import') }}
          </a-button>
        </template>
      </a-table>
    </a-card>
  </div>
  <Files
    v-if="selectedSkillsName !== ''"
    :name="selectedSkillsName"
    :robot="props.robot"
    scope="skills"
    @close="selectedSkillsName = ''"
  />
  <SkillsMarketTable
    v-if="skillsMarketTableVisible"
    :category="props.selectedCategoryItems[0]"
    @close="skillsMarketTableVisible = false"
    @refresh="getSkillsItems"
  />
  <a-modal
    v-model:visible="importSkillsModalVisible"
    :mask-closable="false"
    :title="$t('common.import')"
    :footer="false"
    width="60%"
  >
    <a-upload
      :headers="{ Authorization: `Bearer ${getToken()}` }"
      :show-cancel-button="false"
      accept=".zip"
      name="uf"
      :data="
        props.selectedCategoryItems?.[0] === '#default'
          ? {}
          : { category: props.selectedCategoryItems[0] }
      "
      draggable
      :action="IMPORT_SKILLS_ENDPOINT"
      @success="
        (_) => {
          Message.success(t('common.import.success'));
          getSkillsItems();
        }
      "
      @error="(fileItem) => Message.error(fileItem.response.msg)"
    />
  </a-modal>
  <a-modal
    v-if="props.robot !== ''"
    v-model:visible="robotsImportSkillsModalVisible"
    :mask-closable="false"
    :footer="false"
    width="85%"
  >
    <template #title>
      <a-space>
        <icon-storage />
        <a-space size="large">
          <span>{{ $t('skills.import') }}</span>
          <span>
            <Media
              :style="{
                marginRight: '3px',
                backgroundColor: 'var(--color-bg-2)',
              }"
              :size="25"
              :url="apiGetRobotsManageAvatarUrl({ name: props.robot })"
              scope="avatar"
            />
            {{ props.robot }}
          </span>
          <span>
            <a-avatar
              :size="25"
              :style="{
                marginRight: '3px',
                backgroundColor: generateColor(props.selectedCategoryItems[0]),
              }"
            >
              {{
                props.selectedCategoryItems[0] === '#default'
                  ? '#'
                  : props.selectedCategoryItems[0].charAt(0).toUpperCase() +
                    props.selectedCategoryItems[0].charAt(1)
              }}
            </a-avatar>
            {{
              props.selectedCategoryItems[0] === '#default'
                ? 'default'
                : props.selectedCategoryItems[0]
            }}
          </span>
        </a-space>
      </a-space>
    </template>
    <RobotsManageSkills
      v-if="robotsImportSkillsModalVisible"
      style="height: 80vh; overflow: auto"
      :robot="''"
      :robot-import="true"
      :robot-import-category="props.selectedCategoryItems[0]"
      :robot-import-robot="props.robot"
      @close="robotsImportSkillsModalVisible = false"
      @refresh="getSkillsItems"
    />
  </a-modal>
</template>

<script setup lang="ts">
  import { computed, ref, onMounted, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    apiGetSkillsItems,
    apiDeleteSkills,
    IMPORT_SKILLS_ENDPOINT,
  } from '@/api/skills';
  import {
    apiGetRobotsManageAvatarUrl,
    apiRobotImportSkills,
  } from '@/api/robots/manage';
  import { apiDownloadDir } from '@/api/files';
  import { generateColor } from '@marko19907/string-to-color';
  import Files from '@/components/files/index.vue';
  import RobotsManageSkills from '@/views/skills/index.vue';
  import Media from '@/components/media/index.vue';
  import { getToken } from '@/utils/auth.js';
  import SkillsMarketTable from './skills-market-table.vue';

  const { t } = useI18n();

  const props = defineProps<{
    selectedCategoryItems: string[];
    robot: string;
    robotImport: boolean;
    robotImportCategory: string;
    robotImportRobot: string;
  }>();

  const emit = defineEmits<{ close: []; refresh: [] }>();

  const skillsTableLoading = ref(false);

  const skillsMarketTableVisible = ref(false);
  const importSkillsModalVisible = ref(false);
  const robotsImportSkillsModalVisible = ref(false);

  const isScriptOptions = computed<Record<string, any>[]>(() => [
    {
      label: t('common.true'),
      value: true,
    },
    {
      label: t('common.false'),
      value: false,
    },
  ]);

  const selectedSkillsName = ref('');
  const skillsItems = ref<Record<string, any>[]>([]);
  const skillsTableSelectedKeys = ref<string[]>([]);
  const skillsTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const skillsTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const skillsSearchFormModel = ref<Record<string, any>>({
    name: '',
    description: '',
    isScript: '',
  });

  const skillsTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('skills.name'),
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
      title: t('skills.description'),
      dataIndex: 'description',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('skills.category'),
      dataIndex: 'category',
      ellipsis: true,
      tooltip: true,
      align: 'center',
    },
    {
      title: t('skills.isScript'),
      dataIndex: 'is_script',
      slotName: 'isScript',
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
      width: 310,
    },
  ]);

  // 获取技能列表查询参数
  const getSkillsQueryParams = () => {
    const name = skillsSearchFormModel.value.name.trim();
    const description = skillsSearchFormModel.value.description.trim();
    const { isScript } = skillsSearchFormModel.value;
    const { orderBy, orderType } = skillsTableOrder.value;

    const params: Record<string, any> = {
      page: skillsTablePagination.value.current,
      size: skillsTablePagination.value.pageSize,
    };

    if (name !== '') {
      params.name = name;
    }
    if (description !== '') {
      params.description = description;
    }
    if (isScript !== '') {
      params.is_script = isScript;
    }
    if (props.selectedCategoryItems[0] !== '#default') {
      const category = props.selectedCategoryItems[0];
      params.category = category;
    }

    if (orderBy !== '' && orderType !== '') {
      params.order_by = orderBy;
      params.order_type = orderType;
    }

    if (props.robot !== '') {
      params.robot = props.robot;
    }

    return params;
  };

  // 获取技能列表
  const getSkillsItems = async () => {
    skillsTableLoading.value = true;
    try {
      const params = getSkillsQueryParams();
      const { data } = await apiGetSkillsItems(params);

      skillsItems.value = data.items;
      skillsTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeSkillsTablePage = async (page: number) => {
    skillsTableLoading.value = true;
    skillsTablePagination.value.current = page;
    await getSkillsItems();
    skillsTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeSkillsTablePageSize = async (pageSize: number) => {
    skillsTableLoading.value = true;
    skillsTablePagination.value.pageSize = pageSize;
    await getSkillsItems();
    skillsTableLoading.value = false;
  };

  // 切换表格排序
  const changeSkillsTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    skillsTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      skillsTableOrder.value.orderBy = dataIndex;
      skillsTableOrder.value.orderType =
        direction === 'ascend' ? 'asc' : 'desc';
    } else {
      skillsTableOrder.value.orderBy = '';
      skillsTableOrder.value.orderType = '';
    }
    await getSkillsItems();
    skillsTableLoading.value = false;
  };

  // 删除技能
  const deleteSkills = async (names: string[]) => {
    skillsTableLoading.value = true;
    try {
      const params: Record<string, any> = {
        names,
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }

      await apiDeleteSkills(params);
      await getSkillsItems();
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsTableSelectedKeys.value = [];
      skillsTableLoading.value = false;
    }
  };

  // 重置搜索表单
  const resetSkillsSearchFormModel = async () => {
    skillsTableLoading.value = true;
    skillsSearchFormModel.value.name = '';
    skillsSearchFormModel.value.description = '';
    skillsSearchFormModel.value.isScript = '';
    await getSkillsItems();
    skillsTableLoading.value = false;
  };

  // 导出技能
  const exportSkills = async (name: string) => {
    skillsTableLoading.value = true;
    try {
      const params: Record<string, any> = {
        name,
        scope: 'skills',
      };
      if (props.robot !== '') {
        params.robot = props.robot;
      }
      await apiDownloadDir(params);
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsTableLoading.value = false;
    }
  };

  // 数字员工导入技能
  const robotImportSkills = async (skillsList: string[]) => {
    skillsTableLoading.value = true;
    try {
      const params: Record<string, any> = {
        name: props.robotImportRobot,
        skills_list: skillsList,
      };
      if (props.robotImportCategory !== '#default') {
        params.category = props.robotImportCategory;
      }

      await apiRobotImportSkills(params);
      emit('refresh');
      emit('close');
      Message.success(t('common.import.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      skillsTableLoading.value = false;
    }
  };

  onMounted(() => {
    getSkillsItems();
  });

  watch(
    () => props.selectedCategoryItems[0],
    () => {
      getSkillsItems();
    },
    { deep: true }
  );
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }

  :deep(.arco-table-th) {
    &:last-child {
      .arco-table-th-item-title {
        margin-left: 16px;
      }
    }
  }
</style>
