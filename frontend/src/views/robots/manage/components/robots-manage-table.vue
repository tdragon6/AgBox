<template>
  <a-card style="height: 88vh" :title="$t('robots.manage')">
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="robotsManageSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="16">
            <a-col :span="6">
              <a-form-item field="name" :label="$t('robots.name')">
                <a-input
                  v-model="robotsManageSearchFormModel.name"
                  :placeholder="$t('robots.name.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsManageItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="department" :label="$t('robots.department')">
                <a-input
                  v-model="robotsManageSearchFormModel.department"
                  :placeholder="$t('robots.department.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsManageItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="ranks" :label="$t('robots.rank')">
                <a-select
                  v-model="robotsManageSearchFormModel.ranks"
                  :placeholder="$t('robots.rank.placeholder')"
                  multiple
                  allow-clear
                >
                  <a-option
                    v-for="item in robotsRankOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{ color: robotsRankColor[item.value] }"
                  >
                    <a-tag :color="robotsRankColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="qualities" :label="$t('robots.quality')">
                <a-select
                  v-model="robotsManageSearchFormModel.qualities"
                  :placeholder="$t('robots.quality.placeholder')"
                  multiple
                  allow-clear
                >
                  <a-option
                    v-for="item in robotsQualityOptions"
                    :key="item.value"
                    :value="item.value"
                    :tag-props="{ color: robotsQualityColor[item.value] }"
                  >
                    <a-tag :color="robotsQualityColor[item.value]">
                      {{ item.label }}
                    </a-tag>
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item field="author" :label="$t('robots.author')">
                <a-input
                  v-model="robotsManageSearchFormModel.author"
                  :placeholder="$t('robots.author.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsManageItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="description"
                :label="$t('robots.description')"
              >
                <a-input
                  v-model="robotsManageSearchFormModel.description"
                  :placeholder="$t('robots.description.placeholder')"
                  allow-clear
                  @keyup.enter="getRobotsManageItems"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="createdTime"
                :label="$t('common.time.created')"
              >
                <a-range-picker
                  v-model="robotsManageSearchFormModel.createdTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item
                field="updatedTime"
                :label="$t('common.time.updated')"
              >
                <a-range-picker
                  v-model="robotsManageSearchFormModel.updatedTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
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
            :loading="robotsManageTableLoading"
            type="primary"
            @click="getRobotsManageItems"
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            :loading="robotsManageTableLoading"
            @click="resetRobotsManageSearchFormModel"
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
            @click="importRobotsManageModalVisible = true"
          >
            <template #icon>
              <icon-download />
            </template>
            {{ $t('common.import') }}
          </a-button>
          <a-button
            v-debounce
            size="small"
            type="primary"
            @click="createRobotsManageModalVisible = true"
          >
            <template #icon>
              <icon-plus />
            </template>
            {{ $t('common.create') }}
          </a-button>
        </a-space>
      </a-col>
      <a-col
        :span="12"
        style="display: flex; align-items: center; justify-content: end"
      >
        <a-popconfirm
          type="warning"
          :content="$t('common.confirm.delete')"
          @ok="deleteRobotsManage(robotsManageTableSelectedKeys)"
          @ok-loading="robotsManageTableLoading"
        >
          <a-button
            :disabled="robotsManageTableSelectedKeys.length === 0"
            :loading="robotsManageTableLoading"
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
      </a-col>
    </a-row>
    <a-table
      v-model:selected-keys="robotsManageTableSelectedKeys"
      row-key="name"
      :row-selection="{
        type: 'checkbox',
        showCheckedAll: true,
      }"
      :scroll="{ y: 'calc(88vh - 300px)' }"
      :loading="robotsManageTableLoading"
      :pagination="robotsManageTablePagination"
      :columns="robotsManageTableColumns"
      :data="robotsManageItems"
      :bordered="false"
      @page-change="changeRobotsManageTablePage"
      @page-size-change="changeRobotsManageTablePageSize"
      @sorter-change="changeRobotsManageTableOrder"
    >
      <template #index="{ rowIndex }">
        {{
          rowIndex +
          1 +
          (robotsManageTablePagination.current - 1) *
            robotsManageTablePagination.pageSize
        }}
      </template>
      <template #name="{ record }">
        <span :style="{ display: 'flex', alignItems: 'center' }">
          <a-tooltip :content="$t('robots.avatar.upload')">
            <Media
              :style="{
                marginRight: '8px',
                backgroundColor: 'var(--color-bg-2)',
                cursor: 'pointer',
              }"
              :size="35"
              :url="apiGetRobotsManageAvatarUrl({ name: record.name })"
              scope="avatar"
              @click="
                uploadRobotsManageAvatarModalVisible = true;
                selectedRobotsManageItem = record;
              "
            />
          </a-tooltip>
          {{ record.name }}
        </span>
      </template>
      <template #author="{ record }">
        <a-tag color="arcoblue" bordered>
          {{ record.author }}
        </a-tag>
      </template>
      <template #rank="{ record }">
        <a-tag :color="robotsRankColor[record.rank]" bordered>
          {{ record.rank }}
        </a-tag>
      </template>
      <template #quality="{ record }">
        <a-tag :color="robotsQualityColor[record.quality]" bordered>
          {{ robotsQualityLabel[record.quality] }}
        </a-tag>
      </template>
      <template #createdTime="{ record }">
        {{ dayjs(record.created_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #updatedTime="{ record }">
        {{ dayjs(record.updated_time).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
      <template #operations="{ record }">
        <a-button
          v-debounce
          type="text"
          size="small"
          @click="
            selectedRobotsManageItem = record;
            robotsManageViewModalVisible = true;
          "
        >
          {{ $t('common.view') }}
        </a-button>
        <a-button
          v-debounce
          type="text"
          size="small"
          @click="
            selectedRobotsManageItem = record;
            cloneRobotsManageModalVisible = true;
          "
        >
          {{ $t('robots.manage.clone') }}
        </a-button>
        <a-popconfirm
          type="warning"
          :content="$t('common.confirm.delete')"
          @ok="deleteRobotsManage([record.name])"
          @ok-loading="robotsManageTableLoading"
        >
          <a-button
            :loading="robotsManageTableLoading"
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
          @click="downloadRobotsManage(record)"
        >
          <template #icon>
            <icon-share-internal />
          </template>
          {{ $t('common.export') }}
        </a-button>
      </template>
    </a-table>
  </a-card>
  <a-modal
    v-model:visible="importRobotsManageModalVisible"
    :mask-closable="false"
    :title="$t('common.import')"
    :footer="false"
    width="60%"
  >
    <a-form-item required>
      <ModelConfigSelect v-model:selected-model-config="selectedModelConfig" />
    </a-form-item>
    <a-divider type="dashed" />
    <a-tabs>
      <a-tab-pane key="local" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-download /> {{ $t('robots.import.local') }} </a-space>
        </template>
        <a-upload
          :headers="{ Authorization: `Bearer ${getToken()}` }"
          :show-cancel-button="false"
          accept=".zip"
          name="uf"
          :data="{ model_config_id: selectedModelConfig }"
          draggable
          :action="IMPORT_ROBOTS_MANAGE_ENDPOINT"
          @success="
            (_) => {
              Message.success(t('common.import.success'));
              getRobotsManageItems();
            }
          "
          @error="(fileItem) => Message.error(fileItem.response.msg)"
        />
      </a-tab-pane>
      <a-tab-pane key="github" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-github /> {{ $t('robots.import.github') }} </a-space>
        </template>
        <a-form-item required style="width: 80%">
          <a-input
            v-model="importGithubRepoUrl"
            :placeholder="$t('robots.import.github.placeholder')"
            allow-clear
            style="margin-right: 10px"
            @keyup.enter="importRobotsManageFromGithub"
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            @click="importRobotsManageFromGithub"
          >
            {{ $t('common.import') }}
          </a-button>
        </a-form-item>
      </a-tab-pane>
    </a-tabs>
  </a-modal>
  <a-modal
    v-model:visible="cloneRobotsManageModalVisible"
    :mask-closable="false"
    :title="$t('robots.manage.clone')"
    :ok-loading="robotsManageTableLoading"
    @ok="cloneRobotsManage"
    @cancel="
      cloneRobotsManageName = '';
      selectedRobotsManageItem = {};
    "
  >
    <a-form-item required>
      <a-input
        v-model="cloneRobotsManageName"
        :placeholder="$t('robots.manage.clone.placeholder')"
        allow-clear
        @keyup.enter="cloneRobotsManage"
      />
    </a-form-item>
  </a-modal>
  <a-modal
    v-model:visible="createRobotsManageModalVisible"
    :mask-closable="false"
    :title="$t('common.create')"
    :footer="false"
    width="90%"
  >
    <RobotsManageDetail
      v-if="createRobotsManageModalVisible"
      :selected-robots-manage-item="{}"
      @close="createRobotsManageModalVisible = false"
      @refresh="getRobotsManageItems"
    />
  </a-modal>
  <a-modal
    v-model:visible="robotsManageViewModalVisible"
    :mask-closable="false"
    :footer="false"
    :width="robotsManageViewTabKey === 'skills' ? '90%' : '75%'"
  >
    <template #title>
      <a-space>
        <Media
          :style="{
            marginRight: '3px',
            backgroundColor: 'var(--color-bg-2)',
          }"
          :size="25"
          :url="
            apiGetRobotsManageAvatarUrl({
              name: selectedRobotsManageItem.name,
            })
          "
          scope="avatar"
        />
        {{ selectedRobotsManageItem.name }}
      </a-space>
    </template>
    <a-tabs v-model:active-key="robotsManageViewTabKey">
      <a-tab-pane key="detail" style="margin-top: 10px">
        <template #title>
          <a-space>
            <icon-info-circle /> {{ $t('robots.manage.detail') }}
          </a-space>
        </template>
        <RobotsManageDetail
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'detail'
          "
          :selected-robots-manage-item="selectedRobotsManageItem"
          @refresh="
            async () => {
              await getRobotsManageItems();
              robotsManageViewModalVisible = false;
            }
          "
        />
      </a-tab-pane>
      <a-tab-pane key="skills" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-tool /> {{ $t('skills') }} </a-space>
        </template>
        <RobotsManageSkills
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'skills'
          "
          style="height: 80vh; overflow: auto"
          :robot="selectedRobotsManageItem.name"
          :robot-import="false"
          :robot-import-category="''"
          :robot-import-robot="''"
        />
      </a-tab-pane>
      <a-tab-pane key="rule" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-file /> {{ $t('robots.manage.rule') }} </a-space>
        </template>
        <Editor
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'rule'
          "
          :name="selectedRobotsManageItem.name"
          scope="rule"
          file-path="SOUL.md"
          :robot="''"
        />
      </a-tab-pane>
      <a-tab-pane key="memory" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-history /> {{ $t('robots.manage.memory') }} </a-space>
        </template>
        <Editor
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'memory'
          "
          :name="selectedRobotsManageItem.name"
          scope="memory"
          file-path="MEMORY.md"
          :robot="''"
        />
      </a-tab-pane>
      <a-tab-pane key="config" style="margin-top: 10px">
        <template #title>
          <a-space>
            <icon-settings /> {{ $t('robots.manage.config') }}
          </a-space>
        </template>
        <Editor
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'config'
          "
          :name="selectedRobotsManageItem.name"
          scope="config"
          file-path="config.yaml"
          :robot="''"
        />
      </a-tab-pane>
      <a-tab-pane key="env" style="margin-top: 10px">
        <template #title>
          <a-space> <icon-tag /> {{ $t('robots.manage.env') }} </a-space>
        </template>
        <Editor
          v-if="
            robotsManageViewModalVisible === true &&
            robotsManageViewTabKey === 'env'
          "
          :name="selectedRobotsManageItem.name"
          scope="env"
          file-path=".env"
          :robot="''"
        />
      </a-tab-pane>
    </a-tabs>
  </a-modal>
  <a-modal
    v-model:visible="uploadRobotsManageAvatarModalVisible"
    :mask-closable="false"
    :title="$t('robots.avatar.upload')"
    :footer="false"
    width="60%"
  >
    <a-upload
      :headers="{ Authorization: `Bearer ${getToken()}` }"
      :show-cancel-button="false"
      accept=".png"
      name="uf"
      :data="{ name: selectedRobotsManageItem.name }"
      draggable
      :action="UPLOAD_ROBOTS_MANAGE_AVATAR_ENDPOINT"
      @success="
        (_) => {
          selectedRobotsManageItem = {};
          Message.success(t('robots.avatar.upload.success'));
          uploadRobotsManageAvatarModalVisible = false;
          getRobotsManageItems();
        }
      "
      @error="(fileItem) => Message.error(fileItem.response.msg)"
    />
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { Message } from '@arco-design/web-vue';
  import dayjs from 'dayjs';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import { robotsRankColor, robotsQualityColor } from '@/utils/func';
  import {
    apiGetRobotsManageItems,
    apiDeleteRobotsManage,
    apiCloneRobotsManage,
    apiDownloadRobotsManage,
    apiGetRobotsManageAvatarUrl,
    IMPORT_ROBOTS_MANAGE_ENDPOINT,
    UPLOAD_ROBOTS_MANAGE_AVATAR_ENDPOINT,
  } from '@/api/robots/manage';
  import { apiInstallRobotsMarket } from '@/api/robots/market';
  import ModelConfigSelect from '@/components/model/model-config-select/index.vue';
  import RobotsManageSkills from '@/views/skills/index.vue';
  import Editor from '@/components/files/editor.vue';
  import Media from '@/components/media/index.vue';
  import { getToken } from '@/utils/auth.js';
  import useUnreadRobotsInboxCountStore from '@/store/modules/inbox';
  import RobotsManageDetail from './robots-manage-detail.vue';

  const { t } = useI18n();

  const unreadRobotsInboxCount = useUnreadRobotsInboxCountStore();

  const robotsManageTableLoading = ref(false);

  const cloneRobotsManageModalVisible = ref(false);
  const importRobotsManageModalVisible = ref(false);
  const createRobotsManageModalVisible = ref(false);
  const robotsManageViewModalVisible = ref(false);
  const uploadRobotsManageAvatarModalVisible = ref(false);

  const robotsManageViewTabKey = ref('detail');
  const robotsManageTableSelectedKeys = ref<string[]>([]);
  const selectedModelConfig = ref('');
  const cloneRobotsManageName = ref('');
  const importGithubRepoUrl = ref('');
  const selectedRobotsManageItem = ref<Record<string, any>>({});
  const robotsManageItems = ref<Record<string, any>[]>([]);
  const robotsManageTablePagination = ref<Record<string, any>>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
    showPageSize: true,
    pageSizeOptions: [10, 20, 50, 100],
  });
  const robotsManageTableOrder = ref<Record<string, any>>({
    orderBy: '',
    orderType: '',
  });

  const robotsRankOptions = ref(
    Array.from({ length: 9 }, (_, i) => ({
      label: `L${i + 1}`,
      value: `L${i + 1}`,
    }))
  );

  // 数字员工品质 label
  const robotsQualityLabel: Record<string, any> = {
    common: t('robots.quality.common'),
    uncommon: t('robots.quality.uncommon'),
    epic: t('robots.quality.epic'),
    rare: t('robots.quality.rare'),
    legendary: t('robots.quality.legendary'),
  };

  const robotsQualityOptions = computed<Record<string, any>[]>(() =>
    Object.keys(robotsQualityLabel).map((key) => ({
      value: key,
      label: robotsQualityLabel[key],
    }))
  );

  const robotsManageSearchFormModel = ref<Record<string, any>>({
    name: '',
    description: '',
    author: '',
    department: '',
    ranks: [],
    qualities: [],
    createdTime: [],
    updatedTime: [],
  });

  const robotsManageTableColumns = computed<TableColumnData[]>(() => [
    {
      title: t('common.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 50,
      align: 'center',
    },
    {
      title: t('robots.name'),
      dataIndex: 'name',
      ellipsis: true,
      tooltip: true,
      slotName: 'name',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      width: 300,
    },
    {
      title: t('robots.description'),
      dataIndex: 'description',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('robots.author'),
      dataIndex: 'author',
      ellipsis: true,
      tooltip: true,
      slotName: 'author',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
    },
    {
      title: t('robots.department'),
      dataIndex: 'department',
      ellipsis: true,
      tooltip: true,
      slotName: 'department',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('robots.rank'),
      dataIndex: 'rank',
      slotName: 'rank',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('robots.quality'),
      dataIndex: 'quality',
      slotName: 'quality',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('common.time.created'),
      dataIndex: 'created_time',
      slotName: 'createdTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
        sorter: true,
      },
      align: 'center',
    },
    {
      title: t('common.time.updated'),
      dataIndex: 'updated_time',
      slotName: 'updatedTime',
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
      width: 300,
    },
  ]);

  // 获取数字员工列表查询参数
  const getRobotsManageQueryParams = () => {
    const name = robotsManageSearchFormModel.value.name.trim();
    const description = robotsManageSearchFormModel.value.description.trim();
    const author = robotsManageSearchFormModel.value.author.trim();
    const department = robotsManageSearchFormModel.value.department.trim();
    const { ranks, qualities, createdTime, updatedTime } =
      robotsManageSearchFormModel.value;
    const { orderBy, orderType } = robotsManageTableOrder.value;

    const params: Record<string, any> = {
      page: robotsManageTablePagination.value.current,
      size: robotsManageTablePagination.value.pageSize,
    };

    if (name !== '') {
      params.name = name;
    }
    if (description !== '') {
      params.description = description;
    }
    if (author !== '') {
      params.author = author;
    }
    if (department !== '') {
      params.department = department;
    }
    if (ranks.length !== 0) {
      params.ranks = ranks;
    }
    if (qualities.length !== 0) {
      params.qualities = qualities;
    }
    if (createdTime.length !== 0) {
      [params.start_created_time, params.end_created_time] = createdTime;
    }
    if (updatedTime.length !== 0) {
      [params.start_updated_time, params.end_updated_time] = updatedTime;
    }

    if (orderBy !== '' && orderType !== '') {
      params.order_by = orderBy;
      params.order_type = orderType;
    }

    return params;
  };

  // 获取数字员工列表
  const getRobotsManageItems = async () => {
    robotsManageTableLoading.value = true;
    try {
      const params = getRobotsManageQueryParams();
      const { data } = await apiGetRobotsManageItems(params);

      robotsManageItems.value = data.items;
      robotsManageTablePagination.value.total = data.total;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsManageTableLoading.value = false;
    }
  };

  // 切换表格分页
  const changeRobotsManageTablePage = async (page: number) => {
    robotsManageTableLoading.value = true;
    robotsManageTablePagination.value.current = page;
    await getRobotsManageItems();
    robotsManageTableLoading.value = false;
  };

  // 切换表格每页条数
  const changeRobotsManageTablePageSize = async (pageSize: number) => {
    robotsManageTableLoading.value = true;
    robotsManageTablePagination.value.pageSize = pageSize;
    await getRobotsManageItems();
    robotsManageTableLoading.value = false;
  };

  // 切换表格排序
  const changeRobotsManageTableOrder = async (
    dataIndex: string,
    direction: string
  ) => {
    robotsManageTableLoading.value = true;
    if (direction === 'ascend' || direction === 'descend') {
      robotsManageTableOrder.value.orderBy = dataIndex;
      robotsManageTableOrder.value.orderType =
        direction === 'ascend' ? 'asc' : 'desc';
    } else {
      robotsManageTableOrder.value.orderBy = '';
      robotsManageTableOrder.value.orderType = '';
    }
    await getRobotsManageItems();
    robotsManageTableLoading.value = false;
  };

  // 删除数字员工
  const deleteRobotsManage = async (names: string[]) => {
    robotsManageTableLoading.value = true;
    try {
      const params = {
        names,
      };
      await apiDeleteRobotsManage(params);
      await getRobotsManageItems();
      await unreadRobotsInboxCount.getUnreadRobotsInboxCount();
      Message.success(t('common.delete.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsManageTableSelectedKeys.value = [];
      robotsManageTableLoading.value = false;
    }
  };

  // 重置搜索表单
  const resetRobotsManageSearchFormModel = async () => {
    robotsManageTableLoading.value = true;
    robotsManageSearchFormModel.value.name = '';
    robotsManageSearchFormModel.value.description = '';
    robotsManageSearchFormModel.value.author = '';
    robotsManageSearchFormModel.value.department = '';
    robotsManageSearchFormModel.value.ranks = [];
    robotsManageSearchFormModel.value.qualities = [];
    robotsManageSearchFormModel.value.createdTime = [];
    robotsManageSearchFormModel.value.updatedTime = [];
    await getRobotsManageItems();
    robotsManageTableLoading.value = false;
  };

  // 克隆数字员工
  const cloneRobotsManage = async () => {
    robotsManageTableLoading.value = true;
    try {
      const params = {
        name: selectedRobotsManageItem.value.name,
        clone_name: cloneRobotsManageName.value,
      };
      await apiCloneRobotsManage(params);
      await getRobotsManageItems();
      cloneRobotsManageName.value = '';
      selectedRobotsManageItem.value = {};
      cloneRobotsManageModalVisible.value = false;
      Message.success(t('robots.manage.clone.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsManageTableLoading.value = false;
    }
  };

  // 从 GitHub 导入数字员工
  const importRobotsManageFromGithub = async () => {
    importRobotsManageModalVisible.value = false;
    robotsManageTableLoading.value = true;
    try {
      const params = {
        url: importGithubRepoUrl.value,
        model_config_id: selectedModelConfig.value,
      };
      await apiInstallRobotsMarket(params);
      await getRobotsManageItems();
      importGithubRepoUrl.value = '';
      Message.success(t('common.import.success'));
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsManageTableLoading.value = false;
    }
  };

  // 导出数字员工
  const downloadRobotsManage = async (record: Record<string, any>) => {
    robotsManageTableLoading.value = true;
    try {
      const params = {
        name: record.name,
      };
      await apiDownloadRobotsManage(params);
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      robotsManageTableLoading.value = false;
    }
  };

  onMounted(() => {
    getRobotsManageItems();
  });
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
