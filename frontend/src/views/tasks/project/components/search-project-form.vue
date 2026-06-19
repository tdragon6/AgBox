<template>
  <a-modal
    :visible="true"
    :mask-closable="false"
    width="50%"
    :footer="false"
    @cancel="emit('close')"
  >
    <template #title>
      {{ $t('common.search') }}
    </template>
    <a-row>
      <a-col :flex="1">
        <a-form
          :model="projectSearchFormModel"
          auto-label-width
          label-align="left"
        >
          <a-row :gutter="32">
            <a-col :span="12">
              <a-form-item field="name" :label="$t('tasks.project.name')">
                <a-input
                  v-model="projectSearchFormModel.name"
                  :placeholder="$t('tasks.project.name.placeholder')"
                  allow-clear
                  @keyup.enter="
                    emit('refresh');
                    emit('close');
                  "
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="description"
                :label="$t('tasks.project.description')"
              >
                <a-input
                  v-model="projectSearchFormModel.description"
                  :placeholder="$t('tasks.project.description.placeholder')"
                  allow-clear
                  @keyup.enter="
                    emit('refresh');
                    emit('close');
                  "
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item field="robots" :label="$t('tasks.project.robots')">
                <RobotsSelect
                  v-model:selected-robots="projectSearchFormModel.robots"
                  :multiple="true"
                  :selected-project-item="{}"
                  scope="robot"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="historyRobots"
                :label="$t('tasks.project.robots.history')"
              >
                <RobotsSelect
                  v-model:selected-robots="projectSearchFormModel.historyRobots"
                  :multiple="true"
                  :selected-project-item="{}"
                  scope="robot"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="createTime"
                :label="$t('common.time.created')"
              >
                <a-range-picker
                  v-model="projectSearchFormModel.createTime"
                  show-time
                  :time-picker-props="{
                    defaultValue: ['00:00:00', '00:00:00'],
                  }"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                field="updatedTime"
                :label="$t('common.time.updated')"
              >
                <a-range-picker
                  v-model="projectSearchFormModel.updatedTime"
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
      <a-divider style="height: 135px" direction="vertical" />
      <a-col :flex="'86px'" style="text-align: right">
        <a-space direction="vertical" :size="18">
          <a-button
            v-debounce
            type="primary"
            @click="
              emit('refresh');
              emit('close');
            "
          >
            <template #icon>
              <icon-search />
            </template>
            {{ $t('common.search') }}
          </a-button>
          <a-button
            v-debounce
            @click="
              emit('reset');
              emit('close');
            "
          >
            <template #icon>
              <icon-refresh />
            </template>
            {{ $t('common.reset') }}
          </a-button>
        </a-space>
      </a-col>
    </a-row>
  </a-modal>
</template>

<script setup lang="ts">
  import RobotsSelect from '@/components/robots/robots-select/index.vue';

  const emit = defineEmits<{ close: []; refresh: []; reset: [] }>();

  const projectSearchFormModel = defineModel<Record<string, any>>(
    'projectSearchFormModel',
    {
      default: {
        name: '',
        description: '',
        robots: [],
        historyRobots: [],
        createTime: [],
        updatedTime: [],
      },
    }
  );
</script>
