<template>
  <a-card :title="$t('tasks.scheduler')">
    <a-form :model="schedulerSettingsModelForm" label-align="left">
      <a-form-item field="maxJobs" :label="$t('settings.scheduler.maxJobs')">
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-input-number
            v-model="schedulerSettingsModelForm.maxJobs"
            :placeholder="$t('settings.scheduler.maxJobs.placeholder')"
            allow-clear
            :min="1"
            :max="10000"
            @keyup.enter="
              async () => {
                maxJobsSettingsLoading = true;
                await setSettings(
                  'SCHEDULER_MAX_JOBS',
                  schedulerSettingsModelForm.maxJobs,
                  schedulerSettingsDefaultValue.maxJobs,
                  $t('common.save.success')
                );
                maxJobsSettingsLoading = false;
              }
            "
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="maxJobsSettingsLoading"
            @click="
              async () => {
                maxJobsSettingsLoading = true;
                await setSettings(
                  'SCHEDULER_MAX_JOBS',
                  schedulerSettingsModelForm.maxJobs,
                  schedulerSettingsDefaultValue.maxJobs,
                  $t('common.save.success')
                );
                maxJobsSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
      <a-form-item field="coalesce" :label="$t('settings.scheduler.Coalesce')">
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-switch
            v-model="schedulerSettingsModelForm.coalesce"
            type="round"
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="coalesceSettingsLoading"
            @click="
              async () => {
                coalesceSettingsLoading = true;
                await setSettings(
                  'SCHEDULER_COALESCE',
                  schedulerSettingsModelForm.coalesce,
                  schedulerSettingsDefaultValue.coalesce,
                  $t('common.save.success')
                );
                coalesceSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
      <a-form-item
        field="maxInstances"
        :label="$t('settings.scheduler.maxInstances')"
      >
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-input-number
            v-model="schedulerSettingsModelForm.maxInstances"
            :placeholder="$t('settings.scheduler.maxInstances.placeholder')"
            allow-clear
            :min="1"
            :max="10000"
            @keyup.enter="
              async () => {
                maxInstancesSettingsLoading = true;
                await setSettings(
                  'SCHEDULER_MAX_INSTANCES',
                  schedulerSettingsModelForm.maxInstances,
                  schedulerSettingsDefaultValue.maxInstances,
                  $t('common.save.success')
                );
                maxInstancesSettingsLoading = false;
              }
            "
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="maxInstancesSettingsLoading"
            @click="
              async () => {
                maxInstancesSettingsLoading = true;
                await setSettings(
                  'SCHEDULER_MAX_INSTANCES',
                  schedulerSettingsModelForm.maxInstances,
                  schedulerSettingsDefaultValue.maxInstances,
                  $t('common.save.success')
                );
                maxInstancesSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { getSettings, setSettings } from '@/views/settings/utils/settings';

  const schedulerSettingsDefaultValue = {
    maxJobs: 10,
    coalesce: false,
    maxInstances: 1,
  };

  const schedulerSettingsModelForm = ref({
    maxJobs: schedulerSettingsDefaultValue.maxJobs,
    coalesce: schedulerSettingsDefaultValue.coalesce,
    maxInstances: schedulerSettingsDefaultValue.maxInstances,
  });

  const maxJobsSettingsLoading = ref(false);
  const coalesceSettingsLoading = ref(false);
  const maxInstancesSettingsLoading = ref(false);

  onMounted(async () => {
    maxJobsSettingsLoading.value = true;
    coalesceSettingsLoading.value = true;
    maxInstancesSettingsLoading.value = true;
    schedulerSettingsModelForm.value.maxJobs = await getSettings(
      'SCHEDULER_MAX_JOBS',
      schedulerSettingsDefaultValue.maxJobs
    );
    schedulerSettingsModelForm.value.coalesce = await getSettings(
      'SCHEDULER_COALESCE',
      schedulerSettingsDefaultValue.coalesce
    );
    schedulerSettingsModelForm.value.maxInstances = await getSettings(
      'SCHEDULER_MAX_INSTANCES',
      schedulerSettingsDefaultValue.maxInstances
    );
    maxJobsSettingsLoading.value = false;
    coalesceSettingsLoading.value = false;
    maxInstancesSettingsLoading.value = false;
  });
</script>
