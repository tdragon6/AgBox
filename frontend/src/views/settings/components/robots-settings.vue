<template>
  <a-card :title="$t('robots')">
    <a-form
      :model="robotsSettingsModelForm"
      label-align="left"
      :label-col-props="{ span: 10 }"
      :wrapper-col-props="{ span: 14 }"
    >
      <a-form-item field="overwrite" :label="$t('settings.robots.overwrite')">
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-select
            v-model="robotsSettingsModelForm.overwrite"
            :options="robotsSettingsOverwriteOptions"
            :placeholder="$t('settings.robots.overwrite.select.placeholder')"
            allow-clear
          >
            <template #label="{ data }">
              <a-badge
                :text="$t(data.label)"
                :status="
                  data.value === true
                    ? 'success'
                    : data.value === false
                    ? 'normal'
                    : 'danger'
                "
              />
            </template>
            <template #option="{ data }">
              <a-badge
                :text="$t(data.label)"
                :status="
                  data.value === true
                    ? 'success'
                    : data.value === false
                    ? 'normal'
                    : 'danger'
                "
              />
            </template>
          </a-select>
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="overwriteSettingsLoading"
            @click="
              async () => {
                overwriteSettingsLoading = true;
                await setSettings(
                  'ROBOTS_OVERWRITE',
                  robotsSettingsModelForm.overwrite,
                  robotsSettingsDefaultValue.overwrite,
                  $t('common.save.success')
                );
                overwriteSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
      <a-form-item
        field="formatCheck"
        :label="$t('settings.robots.formatCheck')"
      >
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-switch
            v-model="robotsSettingsModelForm.formatCheck"
            type="round"
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="formatCheckSettingsLoading"
            @click="
              async () => {
                formatCheckSettingsLoading = true;
                await setSettings(
                  'ROBOTS_FORMAT_CHECK',
                  robotsSettingsModelForm.formatCheck,
                  robotsSettingsDefaultValue.formatCheck,
                  $t('common.save.success')
                );
                formatCheckSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
      <a-form-item
        field="createImportHermesSelfSkills"
        :label="$t('settings.robots.createImportHermesSelfSkills')"
      >
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-switch
            v-model="robotsSettingsModelForm.createImportHermesSelfSkills"
            type="round"
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="createImportHermesSelfSkillsSettingsLoading"
            @click="
              async () => {
                createImportHermesSelfSkillsSettingsLoading = true;
                await setSettings(
                  'ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS',
                  robotsSettingsModelForm.createImportHermesSelfSkills,
                  robotsSettingsDefaultValue.createImportHermesSelfSkills,
                  $t('common.save.success')
                );
                createImportHermesSelfSkillsSettingsLoading = false;
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
  import { ref, computed, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { getSettings, setSettings } from '@/views/settings/utils/settings';

  const { t } = useI18n();

  const robotsSettingsDefaultValue: Record<string, any> = {
    overwrite: 'intercept',
    formatCheck: true,
    createImportHermesSelfSkills: true,
  };

  const robotsSettingsModelForm = ref<Record<string, any>>({
    overwrite: robotsSettingsDefaultValue.overwrite,
    formatCheck: robotsSettingsDefaultValue.formatCheck,
    createImportHermesSelfSkills:
      robotsSettingsDefaultValue.createImportHermesSelfSkills,
  });

  const overwriteSettingsLoading = ref(false);
  const formatCheckSettingsLoading = ref(false);
  const createImportHermesSelfSkillsSettingsLoading = ref(false);

  const robotsSettingsOverwriteOptions = computed<Record<string, any>[]>(() => [
    {
      label: t('common.true'),
      value: true,
    },
    {
      label: t('common.false'),
      value: false,
    },
    {
      label: t('common.intercept'),
      value: 'intercept',
    },
  ]);

  onMounted(async () => {
    overwriteSettingsLoading.value = true;
    formatCheckSettingsLoading.value = true;
    createImportHermesSelfSkillsSettingsLoading.value = true;
    robotsSettingsModelForm.value.overwrite = await getSettings(
      'ROBOTS_OVERWRITE',
      robotsSettingsDefaultValue.overwrite
    );
    robotsSettingsModelForm.value.formatCheck = await getSettings(
      'ROBOTS_FORMAT_CHECK',
      robotsSettingsDefaultValue.formatCheck
    );
    robotsSettingsModelForm.value.createImportHermesSelfSkills =
      await getSettings(
        'ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS',
        robotsSettingsDefaultValue.createImportHermesSelfSkills
      );
    overwriteSettingsLoading.value = false;
    formatCheckSettingsLoading.value = false;
    createImportHermesSelfSkillsSettingsLoading.value = false;
  });
</script>
